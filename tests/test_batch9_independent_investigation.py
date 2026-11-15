"""Regression tests for Batch 9 synthetic investigation assessment."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch9_independent_investigation.py"
spec = importlib.util.spec_from_file_location("academy_batch9", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class Batch9Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "new-workspace"
        mod.initialize(self.workspace)

    def test_initial_score_is_zero_and_evidence_intact(self):
        result = mod.grade(self.workspace)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["pass_objective"])
        self.assertTrue(all(c["evidence_intact"] for c in result["cases"].values()))

    def test_perfect_answer_scores_fifteen_without_grading_prose(self):
        path = self.workspace / "answers.json"
        answers = json.loads(path.read_text(encoding="utf-8"))
        for key, case in mod.CASES.items():
            answers[key].update(dict(zip(mod.FIELDS, case["answer"])))
        path.write_text(json.dumps(answers), encoding="utf-8")
        result = mod.grade(self.workspace)
        self.assertEqual(result["score"], 15)
        self.assertTrue(result["pass_objective"])
        self.assertTrue(all(not c["reasoning_present_not_graded"] for c in result["cases"].values()))

    def test_mutated_evidence_invalidates_one_case(self):
        path = self.workspace / "windows.txt"
        path.write_text(path.read_text(encoding="utf-8") + "modified", encoding="utf-8")
        result = mod.grade(self.workspace)
        self.assertFalse(result["cases"]["windows"]["evidence_intact"])
        self.assertEqual(result["cases"]["windows"]["objective_points"], 0)

    def test_init_does_not_overwrite_existing_folder(self):
        with self.assertRaises(FileExistsError):
            mod.initialize(self.workspace)

    def test_invalid_answer_payload_does_not_break_all_cases(self):
        path = self.workspace / "answers.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["web"] = "invalid"
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(mod.grade(self.workspace)["score"], 0)

    def test_each_case_has_three_valid_unique_options(self):
        for case in mod.CASES.values():
            for options, solution in zip(("diagnoses", "actions", "tests"), case["answer"]):
                self.assertEqual(len(case[options]), 3)
                self.assertEqual(len(set(case[options])), 3)
                self.assertIn(solution, case[options])


if __name__ == "__main__":
    unittest.main()
