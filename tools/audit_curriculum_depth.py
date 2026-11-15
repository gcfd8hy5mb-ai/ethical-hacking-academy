#!/usr/bin/env python3
"""Read-only audit of the existing 26-course Ethical Hacking curriculum.

Does not update lessons, IDs, student progress, scores, Firebase, or files.
Calculates descriptive metrics only; word count is not academic sign-off.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

WORDS = re.compile(r"\b[\w]+(?:[-’'][\w]+)*\b", flags=re.UNICODE)


def audit(data: dict) -> dict:
    courses = data.get("courses")
    if not isinstance(courses, list):
        raise ValueError("Expected curriculum.courses array")
    summary = []
    for index, course in enumerate(courses, 1):
        if not isinstance(course, dict) or not isinstance(course.get("lessons"), list):
            raise ValueError(f"Invalid course at position {index}")
        records = []
        for position, lesson in enumerate(course["lessons"], 1):
            if not isinstance(lesson, list) or len(lesson) < 6 or not isinstance(lesson[1], str):
                raise ValueError(f"Invalid lesson in course {index}, position {position}")
            body = lesson[1]
            count = len(WORDS.findall(body))
            records.append({"position": position, "title": lesson[0], "words": count,
                            "below_500": count < 500,
                            "practice_keyword_present": bool(re.search(r"workshop|practicum|exercise|lab", body, re.I)),
                            "note": "Keyword presence does not imply an executable or graded practical."})
        summary.append({"course_index": index, "title": course.get("title"),
                        "lesson_count": len(records),
                        "words": sum(x["words"] for x in records),
                        "below_500": sum(x["below_500"] for x in records),
                        "lessons": records})
    return {"source_version": data.get("version"), "courses": len(summary),
            "lessons": sum(c["lesson_count"] for c in summary),
            "instructional_words": sum(c["words"] for c in summary),
            "below_500": sum(c["below_500"] for c in summary),
            "course_details": summary,
            "limitations": [
                "Measures only lesson body at lesson[1]; excludes separate workbooks, exams, hardware supplements and simulations.",
                "Word counts are approximate; richness, factual correctness, command quality and independent mastery need human review.",
                "A lesson containing the word practicum is not proof of functioning practical assessment."
            ]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curriculum", default="curriculum.json")
    args = parser.parse_args()
    data = json.loads(Path(args.curriculum).read_text(encoding="utf-8"))
    print(json.dumps(audit(data), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
