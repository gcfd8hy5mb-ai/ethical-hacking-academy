#!/usr/bin/env python3
"""Offline structural + editorial audit for published lesson/practice integration.

Uses standard library, makes no network requests or file changes.
Usage: python3 tests/audit_practical_mapping.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "coursework-practical-expansion-2026.json",
    "coursework-specific-practice-2026.json",
    "core-lesson-guided-practice-2026.json",
    "core-guided-practice-batch2-2026.json",
    "core-guided-practice-batch3-2026.json",
)
FIELDS = ("heading", "command", "instruction", "interpretation", "task", "safety")


def read_json(name: str) -> dict:
    with (ROOT / name).open(encoding="utf-8") as stream:
        return json.load(stream)


def audit() -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    core = read_json("curriculum.json")
    mapping = read_json("lesson-practical-title-map-2026.json")
    catalog = {name: read_json(name) for name in SOURCES}
    originals = {(c["title"], lesson[0]) for c in core["courses"] for lesson in c["lessons"]}
    mapped_keys: set[tuple[str, str]] = set()
    all_unit_ids: set[str] = set()
    unit_index: dict[tuple[str, str], dict] = {}
    counters: Counter[str] = Counter()

    for filename, data in catalog.items():
        for unit in data["units"]:
            unit_id = unit.get("id")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append(f"{filename}: practical unit without valid id")
                continue
            if unit_id in all_unit_ids:
                errors.append(f"Duplicate practical unit id: {unit_id}")
            all_unit_ids.add(unit_id)
            if not unit.get("scenario"):
                errors.append(f"{filename}/{unit_id}: missing scenario")
            for section in unit.get("sections", []):
                section_id = section.get("id")
                if not section_id:
                    errors.append(f"{filename}/{unit_id}: missing section id")
                    continue
                identifier = (filename, unit_id + "/" + section_id)
                if identifier in unit_index:
                    errors.append(f"Duplicate practical section: {identifier}")
                unit_index[identifier] = section
                for field in FIELDS:
                    value = section.get(field)
                    if not isinstance(value, str) or len(value.strip()) < 6:
                        errors.append(f"{filename}/{unit_id}/{section_id}: missing/short {field}")
                # Editorial guidance only: brevity is not a proof of incorrect instruction.
                if (len(section.get("instruction", "")) < 90
                        or len(section.get("task", "")) < 65
                        or len(section.get("interpretation", "")) < 60):
                    warnings.append(f"{filename}/{unit_id}/{section_id}: brief guidance; manual review advisable")

    for item in mapping["mappings"]:
        pair = (item["course"], item["lesson"])
        if pair in mapped_keys:
            errors.append(f"Duplicate course/lesson map: {pair}")
        mapped_keys.add(pair)
        filename = item.get("source") or SOURCES[0]
        if filename not in catalog:
            errors.append(f"{pair}: source is not allowlisted ({filename})")
            continue
        key = (filename, str(item.get("unitId", "")) + "/" + str(item.get("sectionId", "")))
        if key not in unit_index:
            errors.append(f"{pair}: missing source unit/section {key}")
        else:
            counters[filename] += 1
        # For exact-match core course titles, require that core lesson exists;
        # supplementary lessons may legitimately be outside the main catalog.
        if pair[0] in {c["title"] for c in core["courses"]} and pair not in originals:
            warnings.append(f"Supplement-only lesson in a core course: {pair}")

    uncovered = originals - mapped_keys
    for pair in sorted(uncovered):
        errors.append(f"Core lesson has no practice: {pair}")
    summary = {
        "core_courses": len(core["courses"]),
        "core_lessons": len(originals),
        "mapped_core_lessons": len(originals & mapped_keys),
        "uncovered_core_lessons": len(uncovered),
        "mapping_rows": len(mapping["mappings"]),
        "unique_units": len(all_unit_ids),
        "source_mapping_counts": dict(counters),
        "editorial_warnings": len(warnings),
    }
    return errors, warnings, summary


def main() -> int:
    errors, warnings, summary = audit()
    print(json.dumps(summary, indent=2))
    print(f"Structural errors: {len(errors)}; editorial warnings: {len(warnings)}")
    for issue in errors[:30]:
        print("ERROR:", issue)
    for note in warnings[:15]:
        print("REVIEW:", note)
    if len(warnings) > 15:
        print(f"...and {len(warnings) - 15} additional editorial items")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
