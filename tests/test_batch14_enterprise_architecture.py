"""Batch 14 enterprise defense simulator regression tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch14_enterprise_architecture.py"
spec = importlib.util.spec_from_file_location("batch14", SCRIPT)
lab = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(lab)


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.folder = Path(t.name) / "new-workspace"
        lab.initialize(self.folder)

    def test_initial_score_zero(self):
        result = lab.grade(self.folder)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["objective_pass"])

    def test_complete_correct_policy_eight(self):
        for control in lab.CONTROLS:
            lab.enable(self.folder, control)
        for event in lab.EVENTS:
            lab.detect(self.folder, event)
        result = lab.grade(self.folder)
        self.assertEqual(result["score"], 8)
        self.assertTrue(result["objective_pass"])

    def test_detections_without_controls_do_not_score(self):
        for event in lab.EVENTS:
            lab.detect(self.folder, event)
        self.assertEqual(lab.grade(self.folder)["score"], 0)

    def test_controls_without_telemetry_score_four(self):
        for control in lab.CONTROLS:
            lab.enable(self.folder, control)
        self.assertEqual(lab.grade(self.folder)["score"], 4)

    def test_refuse_workspace_overwrite(self):
        with self.assertRaises(ValueError):
            lab.initialize(self.folder)

    def test_invalid_control_rejected(self):
        with self.assertRaises(ValueError):
            lab.enable(self.folder, "allow_everyone")

    def test_invalid_data_rejected(self):
        (self.folder / "policy.json").write_text('{"enabled":["unknown"],"observations":[]}')
        with self.assertRaises(ValueError):
            lab.read_state(self.folder)

    def test_inspection_never_exposes_real_endpoint(self):
        snapshot = lab.observe(lab.read_state(self.folder))
        self.assertEqual(len(snapshot["nodes"]), 6)
        self.assertEqual(len(snapshot["access"]), 4)
        self.assertNotIn("http", json.dumps(snapshot))

if __name__ == "__main__":
    unittest.main()
