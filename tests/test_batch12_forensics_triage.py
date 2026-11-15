"""Regression tests for Batch 12 inert forensics and recovery lab."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"local-vm-labs"/"batch12_forensics_triage.py"
spec=importlib.util.spec_from_file_location("batch12",SCRIPT)
lab=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(lab)

class ForensicsTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder=Path(tmp.name)/"new-case"
        lab.build(self.folder)

    def test_four_inert_cases_and_integrity(self):
        evidence,intact=lab.inspect(self.folder)
        self.assertEqual(len(evidence),4)
        self.assertTrue(intact)
        self.assertTrue(all(isinstance(c["artifact"],str) for c in evidence.values()))

    def test_blank_answers_zero(self):
        result=lab.assess(self.folder)
        self.assertEqual(result["score"],0)
        self.assertFalse(result["objective_pass"])

    def test_perfect_selection_twelve(self):
        path=self.folder/"answers.json"
        answers=json.loads(path.read_text())
        for key,case in lab.CASES.items():
            for field in lab.FIELDS:
                answers[key][field]=case[field]
        path.write_text(json.dumps(answers))
        result=lab.assess(self.folder)
        self.assertEqual(result["score"],12)
        self.assertTrue(result["objective_pass"])
        self.assertFalse(any(c["reasoning_length_only"] for c in result["cases"].values()))

    def test_tampering_invalidates_score(self):
        evidence=self.folder/"evidence.json"
        evidence.write_text(evidence.read_text()+"\n")
        result=lab.assess(self.folder)
        self.assertFalse(result["evidence_intact"])
        self.assertEqual(result["score"],0)

    def test_refuse_existing_workspace(self):
        with self.assertRaises(ValueError):
            lab.build(self.folder)

    def test_option_sets_match_known_answers(self):
        opts=lab.choice_options()
        for field in lab.FIELDS:
            self.assertEqual(len(opts[field]),4)
            self.assertEqual(set(opts[field]),{case[field] for case in lab.CASES.values()})

    def test_reject_bad_answer_structure(self):
        (self.folder/"answers.json").write_text("[]")
        with self.assertRaises(ValueError):
            lab.assess(self.folder)

if __name__=="__main__":
    unittest.main()
