"""Batch 13 offline security assessment lab regression checks."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"local-vm-labs"/"batch13_assessment_reporting.py"
spec=importlib.util.spec_from_file_location("batch13",SCRIPT)
lab=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(lab)

class AssessmentTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder=Path(tmp.name)/"fresh"
        lab.init(self.folder)

    def test_four_cases_and_valid_evidence(self):
        evidence,valid=lab.read_evidence(self.folder)
        self.assertEqual(len(evidence),4)
        self.assertTrue(valid)

    def test_blank_submission_zero(self):
        self.assertEqual(lab.assess(self.folder)["score"],0)

    def test_correct_selections_sixteen(self):
        file=self.folder/"answers.json"
        answers=json.loads(file.read_text(encoding="utf-8"))
        for key,case in lab.CASES.items():
            for field in lab.FIELDS:
                answers[key][field]=case[field]
        file.write_text(json.dumps(answers),encoding="utf-8")
        result=lab.assess(self.folder)
        self.assertEqual(result["score"],16)
        self.assertTrue(result["objective_pass"])
        self.assertFalse(any(c["written_reasoning_present_not_graded"] for c in result["cases"].values()))

    def test_tampered_evidence_invalidates_all_answers(self):
        file=self.folder/"evidence.json"
        file.write_text(file.read_text(encoding="utf-8")+"\n",encoding="utf-8")
        self.assertEqual(lab.assess(self.folder)["score"],0)
        self.assertFalse(lab.assess(self.folder)["evidence_integrity"])

    def test_workspace_never_overwritten(self):
        with self.assertRaises(ValueError): lab.init(self.folder)

    def test_all_option_sets_cover_expected_values(self):
        available=lab.options()
        for field in lab.FIELDS:
            self.assertEqual(set(available[field]),{c[field] for c in lab.CASES.values()})

    def test_report_includes_limits_and_all_four_cases(self):
        result=lab.report(self.folder)
        self.assertIn("no real hosts",result)
        for key in lab.CASES:
            self.assertIn(key.replace("_"," ").title(),result)

    def test_reject_invalid_answer_structure(self):
        (self.folder/"answers.json").write_text("[]",encoding="utf-8")
        with self.assertRaises(ValueError): lab.assess(self.folder)

if __name__=="__main__":
    unittest.main()
