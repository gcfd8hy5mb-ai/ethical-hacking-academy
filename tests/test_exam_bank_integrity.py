"""Read-only assessment integrity checks for the existing 24 academy exams.

These are structural checks, not proof of exam difficulty or practical mastery.
Run: python -m unittest discover -s tests -p test_exam_bank_integrity.py -v
"""
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
CURRICULUM=json.loads((ROOT/"curriculum.json").read_text(encoding="utf-8"))
EXAMS=json.loads((ROOT/"exams.json").read_text(encoding="utf-8"))


class ExamBankIntegrityTests(unittest.TestCase):
    def test_all_core_courses_named_in_exam_coverage(self):
        titles={c["title"] for c in CURRICULUM["courses"]}
        assessed={name for exam in EXAMS["exams"] for name in exam["courses"]}
        self.assertEqual(titles-assessed,set())

    def test_exam_and_question_count(self):
        self.assertEqual(len(EXAMS["exams"]),24)
        self.assertEqual(sum(len(exam["questions"]) for exam in EXAMS["exams"]),175)

    def test_question_integrity_and_balanced_answers(self):
        prompts=[]
        positions=Counter()
        for exam in EXAMS["exams"]:
            self.assertTrue(exam["courses"])
            for question in exam["questions"]:
                self.assertEqual(len(question),4)
                prompt,options,correct,explanation=question
                self.assertTrue(prompt.strip())
                self.assertTrue(explanation.strip())
                self.assertEqual(len(options),3)
                self.assertEqual(len({choice.strip().casefold() for choice in options}),3)
                self.assertIn(correct,(0,1,2))
                self.assertTrue(options[correct].strip())
                prompts.append(prompt.strip().casefold())
                positions[correct]+=1
        self.assertEqual(len(prompts),len(set(prompts)))
        self.assertEqual(positions,Counter({0:59,1:58,2:58}))

    def test_obviously_unrelated_distractions_removed(self):
        for exam in EXAMS["exams"]:
            for question in exam["questions"]:
                for option in question[1]:
                    self.assertNotIn("wallpaper",option.lower())


if __name__=="__main__":
    unittest.main()
