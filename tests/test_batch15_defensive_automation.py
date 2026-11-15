"""Batch 15 objective defensive automation regression checks."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch15_defensive_automation.py"
spec = importlib.util.spec_from_file_location("batch15", SCRIPT)
lab = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(lab)


class DefensiveAutomationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "new-workspace"
        lab.initialize(self.folder)

    def test_four_assets_and_integrity(self):
        inventory, intact = lab.inspect(self.folder)
        self.assertTrue(intact)
        self.assertEqual(len(inventory), 4)

    def test_blank_zero(self):
        self.assertEqual(lab.grade(self.folder)["score"], 0)

    def test_correct_twelve(self):
        p = self.folder / "answers.json"
        answers = json.loads(p.read_text(encoding="utf-8"))
        for key, case in lab.CASES.items():
            for field in lab.FIELDS:
                answers[key][field] = case[field]
        p.write_text(json.dumps(answers), encoding="utf-8")
        scored = lab.grade(self.folder)
        self.assertEqual(scored["score"], 12)
        self.assertTrue(scored["objective_pass"])
        self.assertFalse(any(c["written_reasoning_present_not_graded"] for c in scored["cases"].values()))

    def test_modified_inventory_fails_integrity(self):
        p = self.folder / "inventory.json"
        p.write_text(p.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        scored = lab.grade(self.folder)
        self.assertEqual(scored["score"], 0)
        self.assertFalse(scored["objective_pass"])

    def test_existing_folder_not_overwritten(self):
        with self.assertRaises(ValueError):
            lab.initialize(self.folder)

    def test_options_complete_and_finite(self):
        choices = lab.options()
        for field in lab.FIELDS:
            self.assertEqual(set(choices[field]), {case[field] for case in lab.CASES.values()})

    def test_invalid_answers_rejected(self):
        (self.folder / "answers.json").write_text("[]", encoding="utf-8")
        with self.assertRaises(ValueError):
            lab.grade(self.folder)


if __name__ == "__main__":
    unittest.main()
