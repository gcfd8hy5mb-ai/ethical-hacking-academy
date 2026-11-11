"""Batch 6 offline network triage and report regression checks."""
import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch6_security_triage.py"
spec = importlib.util.spec_from_file_location("batch6_triage", SOURCE)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class Batch6TriageTests(unittest.TestCase):
    def test_fictional_log_counts(self):
        evidence = lab.summarize()
        self.assertEqual(evidence["records"], 5)
        self.assertEqual(evidence["outcomes"], {"allow": 2, "deny": 2, "timeout": 1})
        self.assertTrue(all(
            event["src"].startswith("192.0.2.") and event["dst"].startswith("198.51.100.")
            for event in lab.LOGS
        ))
    def test_priority_and_objective_check(self):
        ranked = lab.priorities()
        self.assertEqual(ranked[0]["id"], "WEB-01")
        self.assertEqual(ranked[0]["teaching_score"], 9)
        correct = lab.check_answers(2, 1, "WEB-01")
        self.assertEqual(correct["score_out_of_3"], 3)
        self.assertTrue(correct["passed"])
        wrong = lab.check_answers(5, 0, "NET-01")
        self.assertFalse(wrong["passed"])
        self.assertEqual(wrong["score_out_of_3"], 0)
    def test_professional_reporting_boundaries(self):
        report = lab.report()
        self.assertEqual(len(report["ranked_findings"]), 3)
        self.assertEqual(len(report["required_human_review"]), 4)
        self.assertIn("fictional", report["scope"])

if __name__ == "__main__":
    unittest.main()
