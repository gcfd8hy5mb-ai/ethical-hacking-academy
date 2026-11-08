#!/usr/bin/env python3
"""Regression tests for the offline, self-reported Linux training evidence reviewer."""
from __future__ import annotations

import importlib.util
import os
import stat
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "local-vm-labs" / "academy_evidence_review.py"
spec = importlib.util.spec_from_file_location("academy_evidence_review", SCRIPT)
review = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(review)


class OfflineEvidenceReviewerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="academy-evidence-test-")
        self.addCleanup(self.temp.cleanup)
        self.previous = review.BASE
        self.addCleanup(setattr, review, "BASE", self.previous)
        review.BASE = Path(self.temp.name) / "academy-local-lab"
        for folder in ("permissions", "logs", "config"):
            (review.BASE / folder).mkdir(parents=True)
        (review.BASE / "permissions/report.txt").write_text("TRAINING REPORT\n", encoding="utf-8")
        os.chmod(review.BASE / "permissions/report.txt", 0o600)
        (review.BASE / "logs/resolver.log").write_text(
            "2026-11-07T09:01:00Z ERROR dns timeout querying app.lab.example\n"
            "2026-11-07T09:01:05Z ERROR dns timeout querying app.lab.example\n", encoding="utf-8"
        )
        (review.BASE / "config/web.conf").write_text(
            "server {\n listen 80 extra;\n}\n", encoding="utf-8"
        )

    def write_valid_note(self) -> None:
        (review.BASE / "logs/finding.txt").write_text(
            "OBSERVED: Two DNS timeout entries for app.lab.example appear in the synthetic log.\n"
            "UNKNOWN: The provided events do not prove a compromise or identify the cause.\n"
            "NEXT STEP: Correlate with authorized resolver status, application metrics and maintenance records.\n",
            encoding="utf-8"
        )

    def test_initial_setup_does_not_pass(self) -> None:
        result = review.evaluate()
        self.assertFalse(result["file_check_pass"])
        self.assertFalse(result["checks"]["permissions_mode_0640"])
        self.assertFalse(result["checks"]["config_single_correct_listen_directive"])
        self.assertFalse(result["checks"]["finding_has_observation_section"])

    def test_valid_file_state_and_structured_note_passes(self) -> None:
        self.write_valid_note()
        os.chmod(review.BASE / "permissions/report.txt", 0o640)
        (review.BASE / "config/web.conf").write_text("server {\n listen 80;\n}\n", encoding="utf-8")
        result = review.evaluate()
        self.assertTrue(result["file_check_pass"], result["checks"])
        self.assertEqual(len(result["artifacts"]["logs/resolver.log"]["sha256"]), 64)
        self.assertEqual(result["artifacts"]["permissions/report.txt"]["mode"], "0o640")

    def test_missing_finding_does_not_pass(self) -> None:
        result = review.evaluate()
        self.assertIn("logs/finding.txt", result["artifacts"])
        self.assertIsNotNone(result["artifacts"]["logs/finding.txt"]["error"])

    def test_symlink_to_external_file_is_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("OBSERVED: fake\nUNKNOWN: fake\nNEXT STEP: fake\n", encoding="utf-8")
        (review.BASE / "logs/finding.txt").symlink_to(outside)
        text, error, metadata = review.safe_text("logs/finding.txt")
        self.assertIsNone(text)
        self.assertEqual(error, "Symlinked path refused")
        self.assertFalse(metadata)

    def test_oversized_evidence_is_rejected(self) -> None:
        (review.BASE / "logs/finding.txt").write_text("A" * 32769, encoding="utf-8")
        _, error, _ = review.safe_text("logs/finding.txt")
        self.assertIn("32 KiB limit", error)

    def test_unreadable_utf8_is_rejected(self) -> None:
        (review.BASE / "logs/finding.txt").write_bytes(bytes([255,254]))
        _, error, _ = review.safe_text("logs/finding.txt")
        self.assertIsNotNone(error)

    def test_review_is_read_only(self) -> None:
        self.write_valid_note()
        before = {p.relative_to(review.BASE).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in review.BASE.rglob("*") if p.is_file()}
        review.evaluate()
        after = {p.relative_to(review.BASE).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in review.BASE.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
