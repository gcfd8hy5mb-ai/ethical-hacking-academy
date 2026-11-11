"""Synthetic diagnostic exercise regression: no real network dependency."""
import importlib.util
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/"local-vm-labs"/"batch4_fault_isolation.py"
spec=importlib.util.spec_from_file_location("fault_lab",FILE)
lab=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class FaultIsolationTests(unittest.TestCase):
    def test_four_distinct_cases(self):
        self.assertEqual(set(lab.CASES),{"dns","route","service","permissions"})
        for key,item in lab.CASES.items():
            self.assertGreaterEqual(len(item["evidence"]),3)
            self.assertEqual(set(item["options"]),{"A","B","C"})
            self.assertIn(item["correct"],item["options"])
            self.assertGreater(len(item["reason"]),60)
            self.assertGreater(len(item["limitations"]),40)
    def test_all_answers_have_correct_and_wrong_feedback(self):
        for key,item in lab.CASES.items():
            winner=lab.review(key,item["correct"])
            self.assertTrue(winner["correct"])
            self.assertIn("Practice-only",winner["important"])
            wrong=next(k for k in item["options"] if k!=item["correct"])
            self.assertFalse(lab.review(key,wrong)["correct"])
            self.assertFalse(lab.review(key,"Z")["valid_selection"])

if __name__=="__main__":
    unittest.main()
