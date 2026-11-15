"""Batch 10 real HTTP fixture regression checks (localhost only)."""
from __future__ import annotations

import importlib.util
import json
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest

PATH = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch10_live_defense_practicum.py"
spec = importlib.util.spec_from_file_location("batch10", PATH)
lab = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(lab)


class LiveDefensivePracticumTests(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.folder = Path(td.name) / "fixture"
        lab.initialize(self.folder)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), lab.handler_factory(self.folder))
        self.addCleanup(self.server.server_close)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.shutdown)
        self.port = self.server.server_port

    def force(self, fault):
        c = lab.read_case(self.folder)
        c.update({"fault": fault, "fixed": False, "diagnosis": None,
                  "attempts": 0, "correct_repairs": 0})
        lab.write_case(self.folder, c)

    def test_each_fault_has_real_distinct_http_symptom(self):
        for fault in lab.FAULTS:
            with self.subTest(fault=fault):
                self.force(fault)
                actual = lab.inspect(self.port)
                self.assertEqual(actual["/private"]["status"], 403)
                if fault == "availability":
                    self.assertEqual(actual["/health"]["status"], 503)
                elif fault == "access":
                    self.assertEqual(actual["/reports"]["status"], 403)
                elif fault == "integrity":
                    self.assertNotEqual(actual["/reports"]["payload"], lab.EXPECTED)
                else:
                    self.assertEqual(actual["/reports"]["cache_control"], "")

    def test_first_diagnosis_and_exact_repair_achieve_ten(self):
        for fault, settings in lab.FAULTS.items():
            with self.subTest(fault=fault):
                self.force(fault)
                lab.submit(self.folder, settings["diagnosis"])
                lab.repair(self.folder, settings["repair"])
                score = lab.grade(self.folder, self.port)
                self.assertEqual(score["score"], 10)
                self.assertTrue(score["pass"])

    def test_wrong_repair_does_not_fix_and_reduces_points(self):
        self.force("integrity")
        lab.submit(self.folder, "bad_application_data")
        lab.repair(self.folder, "restore_service_configuration")
        self.assertFalse(lab.read_case(self.folder)["fixed"])
        lab.repair(self.folder, "restore_expected_fixture_data")
        score = lab.grade(self.folder, self.port)
        self.assertEqual(score["score"], 9)
        self.assertTrue(score["pass"])
        self.assertFalse(score["checks"]["bounded_repair_attempt"])

    def test_first_diagnosis_cannot_be_revised(self):
        lab.submit(self.folder, "service_unavailable")
        with self.assertRaises(ValueError):
            lab.submit(self.folder, "bad_application_data")

    def test_workspace_never_overwritten(self):
        with self.assertRaises(ValueError):
            lab.initialize(self.folder)

    def test_missing_server_does_not_fake_pass(self):
        self.server.shutdown()
        self.server.server_close()
        result = lab.grade(self.folder, self.port)
        self.assertFalse(result["pass"])
        self.assertIsNone(result["observations"]["/health"]["status"])

    def test_an_unrecognized_path_is_not_a_valid_report(self):
        self.assertEqual(lab.request("/not-found", self.port)["status"], 404)


if __name__ == "__main__":
    unittest.main()
