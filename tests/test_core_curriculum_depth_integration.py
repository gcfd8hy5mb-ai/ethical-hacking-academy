"""Regression guards for in-place core lesson enrichment.

Run from repository root:
python3 -m unittest discover -s tests -p test_core_curriculum_depth_integration.py -v
"""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"curriculum.json").read_text(encoding="utf-8"))
NETWORK_TITLES=(
 "Trace a website request end to end",
 "Subnets with a pencil",
 "Model a packet journey",
 "Compare DNS, TCP and HTTP errors",
 "Plan safe network troubleshooting",
 "Write a network diagnosis memo",
)
REPORT_TITLES=(
 "Defining authorized testing scope",
 "Evidence requirements and limitations",
 "Building a target inventory from supplied diagrams",
 "Threat model development",
 "Control validation plans",
 "Risk ranking in business context",
 "Writing reproducible findings",
 "Remediation recommendations",
 "Retest and closure criteria",
 "Executive reporting and presentation",
)


class CurriculumDepthIntegrationTests(unittest.TestCase):
    def test_course_and_lesson_positions_preserved(self):
        courses=DATA["courses"]
        self.assertEqual(len(courses),26)
        self.assertEqual(sum(len(c["lessons"]) for c in courses),198)

    def test_expected_network_lesson_order_and_depth(self):
        course=DATA["courses"][18]
        self.assertEqual(course["title"],"Hands-On Network Reasoning Workshop")
        self.assertEqual(tuple(l[0] for l in course["lessons"]),NETWORK_TITLES)
        self.assertTrue(all("ADVANCED NETWORK FIELD STUDY —" in l[1] for l in course["lessons"]))

    def test_reporting_lesson_order_and_depth(self):
        course=DATA["courses"][24]
        self.assertEqual(course["title"],"Security Assessment and Reporting Workshop")
        self.assertEqual(tuple(l[0] for l in course["lessons"]),REPORT_TITLES)
        self.assertTrue(all("APPLIED REPORTING PRACTICUM —" in l[1] for l in course["lessons"]))

    def test_hardware_device_specific_lesson_depth(self):
        course=DATA["courses"][25]
        self.assertEqual(course["title"],"Ethical Hacking Hardware Foundations")
        self.assertEqual(len(course["lessons"]),20)
        for lesson in course["lessons"]:
            self.assertEqual(lesson[1].count("DEVICE-SPECIFIC MASTERY EXPANSION —"),1)
            self.assertIn("INTERPRETING EVIDENCE AND TROUBLESHOOTING:",lesson[1])
            self.assertIn("INDEPENDENT MASTERY ASSIGNMENT:",lesson[1])

    def test_identity_lesson_depth(self):
        course=DATA["courses"][6]
        self.assertEqual(course["title"],"Digital Identity and Everyday Security")
        self.assertEqual(len(course["lessons"]),6)
        for lesson in course["lessons"]:
            self.assertEqual(lesson[1].count("IDENTITY-SECURITY MASTERY EXPANSION —"),1)
            self.assertIn("GUIDED SAFE PRACTICE:",lesson[1])

    def test_existing_quiz_schema_kept(self):
        for course in DATA["courses"]:
            for lesson in course["lessons"]:
                self.assertGreaterEqual(len(lesson),6)
                self.assertIsInstance(lesson[2],str)
                self.assertIsInstance(lesson[3],list)
                self.assertGreater(len(lesson[3]),0)
                self.assertIsInstance(lesson[4],int)
                self.assertTrue(0<=lesson[4]<len(lesson[3]))
                self.assertIsInstance(lesson[5],str)

    def test_new_text_not_blank_or_repeated(self):
        for index,marker in ((18,"ADVANCED NETWORK FIELD STUDY —"),(24,"APPLIED REPORTING PRACTICUM —")):
            bodies=[l[1] for l in DATA["courses"][index]["lessons"]]
            self.assertEqual(len(bodies),len(set(bodies)))
            self.assertTrue(all(body.count(marker)==1 for body in bodies))


if __name__=="__main__":
    unittest.main()
