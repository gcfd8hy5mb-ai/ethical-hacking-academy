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

    def test_all_primary_lesson_bodies_reach_triage_threshold(self):
        import re
        word_pattern=re.compile(r"\\b[\\w]+(?:[-’'][\\w]+)*\\b",flags=re.UNICODE)
        short=[(course["title"],lesson[0])
               for course in DATA["courses"]
               for lesson in course["lessons"]
               if len(word_pattern.findall(lesson[1]))<500]
        self.assertEqual(short,[],f"Lessons needing length triage: {short}")

    def test_remaining_foundation_depth_integrations(self):
        targeted={0:5,1:6,2:6,4:5,12:6,13:5,14:6}
        for index,expected in targeted.items():
            lessons=DATA["courses"][index]["lessons"]
            matches=[l for l in lessons if "FOUNDATION DEPTH INTEGRATION —" in l[1]]
            self.assertEqual(len(matches),expected,DATA["courses"][index]["title"])
            for lesson in matches:
                self.assertEqual(lesson[1].count("FOUNDATION DEPTH INTEGRATION —"),1)
                self.assertIn("WORKED FICTIONAL EXAMPLE:",lesson[1])
                self.assertIn("INDEPENDENT TASK:",lesson[1])

    def test_answer_positions_are_not_predictable(self):
        from collections import Counter
        positions=Counter(lesson[4] for course in DATA["courses"] for lesson in course["lessons"])
        self.assertEqual(positions,Counter({0:66,1:65,2:67}))
        self.assertTrue(all(len(lesson[3])==3 for course in DATA["courses"] for lesson in course["lessons"]))

    def test_unique_question_prompts_and_answer_options(self):
        prompts=[]
        for course in DATA["courses"]:
            for lesson in course["lessons"]:
                prompts.append(lesson[2].strip().casefold())
                options=[x.strip().casefold() for x in lesson[3]]
                self.assertEqual(len(options),len(set(options)),lesson[0])
                self.assertTrue(lesson[3][lesson[4]].strip())
        self.assertEqual(len(prompts),len(set(prompts)))

    def test_network_and_hardware_scaffolding_replaced(self):
        for index, expected in ((2,6),(25,20)):
            lessons=DATA["courses"][index]["lessons"]
            self.assertEqual(len(lessons),expected)
            for lesson in lessons:
                body=lesson[1]
                self.assertEqual(body.count("TOPIC-SPECIFIC TECHNICAL INVESTIGATION —"),1)
                self.assertNotIn("GUIDED ANALYSIS: First identify the actors",body)
                self.assertNotIn("PURPOSE AND RELEVANCE: Explain how this topic",body)
                self.assertIn("INDEPENDENT",body.upper())

    def test_report_workshop_keeps_specific_cases(self):
        for lesson in DATA["courses"][24]["lessons"]:
            self.assertIn("APPLIED REPORTING PRACTICUM —",lesson[1])

    def test_advanced_four_course_scaffold_replacement(self):
        expected={
            20:"Enterprise Identity and Access Management",
            21:"Linux System Administration Lab Theory",
            22:"Web Application Security Fundamentals",
            23:"Cloud Infrastructure Security",
        }
        for index,title in expected.items():
            course=DATA["courses"][index]
            self.assertEqual(course["title"],title)
            self.assertEqual(len(course["lessons"]),10)
            for lesson in course["lessons"]:
                body=lesson[1]
                self.assertEqual(body.count("TOPIC-SPECIFIC VALIDATION CASE —"),1)
                self.assertIn("FICTIONAL OBSERVATION:",body)
                self.assertIn("TECHNICAL INTERPRETATION AND LIMITS:",body)
                self.assertNotIn("GUIDED ANALYSIS: First identify the actors",body)

    def test_linux_terminal_workshops_are_distinct(self):
        course=DATA["courses"][5]
        self.assertEqual(course["title"],"Beginner Linux and Terminal Skills")
        self.assertEqual(len(course["lessons"]),8)
        for lesson in course["lessons"]:
            body=lesson[1]
            self.assertEqual(body.count("LINUX FIELD INVESTIGATION —"),1)
            self.assertIn("INDEPENDENT LAB OR PAPER PRACTICE:",body)
            self.assertNotIn("PURPOSE AND RELEVANCE: Explain how this topic",body)

    def test_incident_response_workshops_are_distinct(self):
        course=DATA["courses"][3]
        self.assertEqual(course["title"],"Security Operations and Incident Response")
        self.assertEqual(len(course["lessons"]),6)
        for lesson in course["lessons"]:
            body=lesson[1]
            self.assertEqual(body.count("INCIDENT EVIDENCE WORKSHOP —"),1)
            self.assertIn("EVIDENCE LIMITATIONS AND POST-FIX VALIDATION:",body)
            self.assertNotIn("PURPOSE AND RELEVANCE: Explain how this topic",body)

    def test_windows_network_and_programming_editorial_repairs(self):
        expected={
            7:("Windows Administration and Security",8),
            8:("Networking Practice and Troubleshooting",8),
            9:("Programming Logic for Security Beginners",8),
            19:("Beginner Python Logic and Defensive Automation",6),
        }
        for index,(title,count) in expected.items():
            course=DATA["courses"][index]
            self.assertEqual(course["title"],title)
            self.assertEqual(len(course["lessons"]),count)
            for lesson in course["lessons"]:
                body=lesson[1]
                self.assertEqual(body.count("PROFESSIONAL FIELD STUDY —"),1)
                self.assertIn("UNDERLYING MECHANISM:",body)
                self.assertIn("WORKED EVIDENCE AND ALTERNATIVE INTERPRETATION:",body)
                self.assertIn("INDEPENDENT PRACTICE:",body)
                self.assertNotIn("PURPOSE AND RELEVANCE: Explain how this topic",body)
                self.assertNotIn("GUIDED ANALYSIS: First identify the actors",body)

    def test_phase9_professional_security_course_rewrites(self):
        target={
            10:"Security Analysis and Professional Practice",
            11:"Defensive Web and Cloud Fundamentals",
            15:"Introduction to Defensive Cryptography",
            16:"Security Monitoring and Log Analysis",
            17:"Safe Authorized Assessment Methodology",
        }
        for index,title in target.items():
            course=DATA["courses"][index]
            self.assertEqual(course["title"],title)
            self.assertEqual(len(course["lessons"]),6)
            for lesson in course["lessons"]:
                body=lesson[1]
                self.assertEqual(body.count("APPLIED SECURITY REVIEW —"),1)
                self.assertIn("MECHANISM AND CONFIDENCE LIMITS:",body)
                self.assertIn("INDEPENDENT ASSIGNMENT:",body)
                self.assertNotIn("PURPOSE AND RELEVANCE: Explain how this topic",body)
                self.assertNotIn("GUIDED ANALYSIS: First identify the actors",body)

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
