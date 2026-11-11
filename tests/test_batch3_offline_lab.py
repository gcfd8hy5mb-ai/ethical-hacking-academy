"""Offline regression tests for Batch 3 practical lab. No network or OS changes."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch3_offline_lab.py"
spec = importlib.util.spec_from_file_location("batch3_lab", SOURCE)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class Batch3LabTests(unittest.TestCase):
    def test_new_workspace_then_readonly_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "new-lab"
            self.assertFalse(folder.exists())
            receipt = lab.init(folder)
            self.assertEqual(len(receipt["files"]), 4)
            self.assertFalse(receipt["network_used"])
            output = lab.check(folder)
            self.assertTrue(output["passed"], output)
            self.assertTrue(output["checks"]["synthetic_event_counts"])
            original = (folder / "events.csv").read_bytes()
            lab.check(folder)
            self.assertEqual((folder / "events.csv").read_bytes(), original)
            with self.assertRaises(ValueError):
                lab.init(folder)  # No overwrite.

    def test_synthetic_log_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "fixture"
            lab.init(folder)
            (folder / "events.csv").write_text("time,user,source,result\n", encoding="utf-8")
            output = lab.check(folder)
            self.assertFalse(output["passed"])
            self.assertFalse(output["checks"]["synthetic_event_counts"])

    def test_missing_files_and_symlinks_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "fixture"
            lab.init(folder)
            (folder / "config/service.txt").unlink()
            self.assertFalse(lab.check(folder)["passed"])
            self.assertFalse(lab.check(folder)["checks"]["readable:config/service.txt"])
            with self.assertRaises(ValueError):
                lab.init(folder)

    def test_reject_root_workspace(self):
        with self.assertRaises(ValueError):
            lab.normal_workspace(Path.cwd().anchor)


if __name__ == "__main__":
    unittest.main()
