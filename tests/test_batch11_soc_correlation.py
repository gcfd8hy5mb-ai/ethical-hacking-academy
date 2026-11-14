"""Tests for offline Batch 11 SOC evidence correlation lab."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch11_soc_correlation.py"
spec = importlib.util.spec_from_file_location("academy_batch11", SCRIPT)
lab = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(lab)


class SocCorrelationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name) / "workspace"
        lab.initialize(self.folder)

    def test_sixteen_events_four_cases_and_valid_digest(self):
        result = lab.analyze(self.folder)
        self.assertEqual(result["total_events"], 16)
        self.assertTrue(result["integrity_matches_manifest"])
        self.assertEqual(len(result["cases"]), 4)
        self.assertEqual(sum(result["source_counts"].values()), 16)

    def test_initial_score_zero(self):
        result = lab.grade(self.folder)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["pass_objective"])
        self.assertTrue(all(item["evidence_integrity"] for item in result["cases"].values()))

    def test_correct_objective_answers_score_twelve(self):
        path = self.folder / "answers.json"
        answers = json.loads(path.read_text(encoding="utf-8"))
        for key, case in lab.SCENARIOS.items():
            for field in lab.FIELDS:
                answers[key][field] = case[field]
        path.write_text(json.dumps(answers), encoding="utf-8")
        result = lab.grade(self.folder)
        self.assertEqual(result["score"], 12)
        self.assertTrue(result["pass_objective"])
        self.assertFalse(result["cases"]["dns_record"]["reasoning_length_only"])

    def test_changed_evidence_invalidates_all_score(self):
        path = self.folder / lab.NAME
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result = lab.grade(self.folder)
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["pass_objective"])

    def test_init_never_overwrites_existing_folder(self):
        with self.assertRaises(ValueError):
            lab.initialize(self.folder)

    def test_options_are_finite_and_include_expected_answers(self):
        for key, case in lab.SCENARIOS.items():
            options = lab.options(key)
            for field in lab.FIELDS:
                self.assertEqual(len(options[field]), 4)
                self.assertIn(case[field], options[field])

    def test_corrupted_answer_payload_is_rejected(self):
        (self.folder / "answers.json").write_text("[]", encoding="utf-8")
        with self.assertRaises(ValueError):
            lab.grade(self.folder)


if __name__ == "__main__":
    unittest.main()
