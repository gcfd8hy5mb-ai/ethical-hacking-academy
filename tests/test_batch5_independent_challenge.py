"""Integration tests for Batch 5 independent diagnosis using actual loopback HTTP."""
from __future__ import annotations
import importlib.util
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "local-vm-labs"
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

service = load("batch5_service_tests", "batch5_local_service.py")
challenge = load("batch5_challenge_tests", "batch5_independent_challenge.py")
EVIDENCE = "The health endpoint and records response differ in HTTP status, so I compared the actual responses against expected readiness and record content."


class IndependentChallengeTests(unittest.TestCase):
    def test_all_three_faults_and_repairs_on_real_loopback(self):
        for fault in challenge.FAULTS:
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temp:
                workspace = Path(temp) / "student"
                service.init(workspace)
                server = ThreadingHTTPServer(("127.0.0.1", 0), service.handler_factory(workspace))
                thread = threading.Thread(target=server.serve_forever,
                                          kwargs={"poll_interval": 0.02}, daemon=True)
                thread.start()
                try:
                    port = server.server_address[1]
                    started = challenge.start(workspace, fault)
                    self.assertTrue(started["started"])
                    self.assertNotIn(fault, started["message"])
                    self.assertFalse(challenge.inspect(workspace, port)["checks"]["records_exact"] if fault != "denied" else challenge.inspect(workspace, port)["checks"]["records_accessible"])
                    with self.assertRaises(ValueError):
                        challenge.start(workspace, fault)
                    with self.assertRaises(ValueError):
                        challenge.diagnose(workspace, fault, "short")
                    response = challenge.diagnose(workspace, fault, EVIDENCE)
                    self.assertTrue(response["diagnosis_correct"])
                    with self.assertRaises(ValueError):
                        challenge.diagnose(workspace, fault, EVIDENCE)
                    before = challenge.grade(workspace, port)
                    self.assertLess(before["objective_score_out_of_6"], 6)
                    service.set_mode(workspace, "healthy")
                    final = challenge.grade(workspace, port)
                    self.assertEqual(final["objective_score_out_of_6"], 6)
                    self.assertTrue(final["fully_repaired"])
                finally:
                    server.shutdown()
                    server.server_close()
                    thread.join(timeout=2)

    def test_wrong_diagnosis_locked_and_safety(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "student"
            service.init(workspace)
            challenge.start(workspace, "stopped")
            wrong = challenge.diagnose(workspace, "bad-data", EVIDENCE)
            self.assertEqual(wrong["diagnosis_points"], 0)
            service.set_mode(workspace, "healthy")
            grade = challenge.grade(workspace, 18765)
            self.assertEqual(grade["diagnosis_points"], 0)
            self.assertFalse(grade["fully_repaired"])  # No running server.
            with self.assertRaises(ValueError):
                challenge.start(workspace, "denied")
            with self.assertRaises(ValueError):
                challenge.grade(Path(temp) / "missing")

if __name__ == "__main__":
    unittest.main()
