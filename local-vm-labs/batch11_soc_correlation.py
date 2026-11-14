#!/usr/bin/env python3
"""Batch 11: offline cross-platform SOC correlation investigation.

Only creates and reads fictional JSONL evidence inside a fresh workspace.
No actual OS log collection, network access, subprocesses, credentials,
administrator permissions, or changes to Academy progress.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

HOSTS = ("win-app-01", "linux-api-01", "resolver-01")
SOURCES = ("windows", "linux", "network", "change")
SCENARIOS = {
    "release_regression": {
        "evidence": [
            ("2026-11-14T12:00:00Z", "change", "win-app-01", "CHG-140 approved update started"),
            ("2026-11-14T12:02:00Z", "windows", "win-app-01", "Service config target path missing"),
            ("2026-11-14T12:04:00Z", "network", "win-app-01", "Health returned HTTP 503"),
            ("2026-11-14T12:05:00Z", "windows", "win-app-01", "Training account single failed sign-in"),
        ],
        "diagnosis": "approved_change_regression",
        "next_check": "compare_approved_change_with_service_config",
        "safe_action": "restore_known_good_training_config",
        "counter": "A failed sign-in alone does not prove account compromise."
    },
    "linux_permission": {
        "evidence": [
            ("2026-11-14T12:00:00Z", "change", "linux-api-01", "Approved service account changed"),
            ("2026-11-14T12:01:00Z", "linux", "linux-api-01", "svc-reader denied traverse on parent"),
            ("2026-11-14T12:02:00Z", "linux", "linux-api-01", "File has allowed read group"),
            ("2026-11-14T12:03:00Z", "network", "linux-api-01", "HTTP 403 on intended report"),
        ],
        "diagnosis": "missing_parent_traverse",
        "next_check": "inspect_parent_mode_and_effective_identity",
        "safe_action": "propose_scoped_acl_with_negative_test",
        "counter": "A readable file is inaccessible if a parent denies traversal."
    },
    "dns_record": {
        "evidence": [
            ("2026-11-14T12:00:00Z", "network", "resolver-01", "NXDOMAIN for api.training.example"),
            ("2026-11-14T12:01:00Z", "network", "linux-api-01", "Direct local fixture health 200"),
            ("2026-11-14T12:03:00Z", "change", "resolver-01", "Approved DNS change pending review"),
            ("2026-11-14T12:05:00Z", "linux", "linux-api-01", "Training service active"),
        ],
        "diagnosis": "missing_dns_record",
        "next_check": "compare_expected_zone_record_to_approved_change",
        "safe_action": "review_and_restore_approved_dns_record",
        "counter": "A DNS failure does not establish malicious redirection."
    },
    "session_revocation": {
        "evidence": [
            ("2026-11-14T12:00:00Z", "change", "win-app-01", "Fictional staff account disabled"),
            ("2026-11-14T12:01:00Z", "windows", "win-app-01", "New password login denied"),
            ("2026-11-14T12:02:00Z", "network", "win-app-01", "Old synthetic session still reads report"),
            ("2026-11-14T12:03:00Z", "change", "win-app-01", "No mock session invalidation recorded"),
        ],
        "diagnosis": "stale_session_after_offboarding",
        "next_check": "verify_old_token_negative_authorization",
        "safe_action": "revoke_training_sessions_and_verify_new_allowed",
        "counter": "Account disabling may not invalidate existing bearer sessions."
    },
}
FIELDS = ("diagnosis", "next_check", "safe_action")
NAME = "synthetic_events.jsonl"


def canonical(raw: str) -> Path:
    path = Path(raw).expanduser().absolute()
    if path == Path(path.anchor) or not path.name:
        raise ValueError("Refusing filesystem root")
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Refusing symlink path")
    return path


def data_path(folder: Path, filename: str) -> Path:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize an authorized disposable workspace")
    path = folder / filename
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 128_000:
        raise ValueError("Missing, unsafe or oversized fixture: " + filename)
    return path


def fixture_rows() -> list[dict]:
    rows = []
    for scenario, case in SCENARIOS.items():
        for index, (time, source, host, observation) in enumerate(case["evidence"]):
            rows.append({"event_id": scenario + "-" + str(index + 1),
                         "scenario": scenario, "time_utc": time,
                         "source": source, "host": host, "observation": observation})
    return rows


def initialize(folder: Path) -> None:
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():
        raise ValueError("Workspace must be a new child of an existing directory")
    folder.mkdir(mode=0o700)
    lines = "".join(json.dumps(row, sort_keys=True) + "\n" for row in fixture_rows())
    (folder / NAME).write_text(lines, encoding="utf-8")
    digest = hashlib.sha256(lines.encode("utf-8")).hexdigest()
    (folder / "manifest.json").write_text(json.dumps({"sha256": digest}, indent=2) + "\n", encoding="utf-8")
    (folder / "answers.json").write_text(json.dumps({
        key: dict.fromkeys((*FIELDS, "reasoning"), "") for key in SCENARIOS
    }, indent=2) + "\n", encoding="utf-8")
    print("Created 16 synthetic events, four cases, checksum manifest, and an editable answer template.")


def read_events(folder: Path) -> tuple[list[dict], bool]:
    content = data_path(folder, NAME).read_bytes()
    manifest = json.loads(data_path(folder, "manifest.json").read_text(encoding="utf-8"))
    valid = isinstance(manifest, dict) and manifest.get("sha256") == hashlib.sha256(content).hexdigest()
    rows = [json.loads(line) for line in content.decode("utf-8").splitlines()]
    if len(rows) != 16 or not all(isinstance(r, dict) and r.get("source") in SOURCES
                                   and r.get("host") in HOSTS for r in rows):
        raise ValueError("Evidence shape changed")
    return rows, valid


def analyze(folder: Path) -> dict:
    rows, valid = read_events(folder)
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["scenario"]].append(row)
    return {"integrity_matches_manifest": valid,
            "total_events": len(rows),
            "source_counts": dict(sorted(Counter(r["source"] for r in rows).items())),
            "cases": {key: {"events": grouped[key]} for key in SCENARIOS},
            "warning": "Synthetic correlation demonstrates reasoning, not actual system compromise."}


def options(case_id: str) -> dict:
    case = SCENARIOS[case_id]
    return {"case": case_id,
            "diagnosis": sorted({c["diagnosis"] for c in SCENARIOS.values()}),
            "next_check": sorted({c["next_check"] for c in SCENARIOS.values()}),
            "safe_action": sorted({c["safe_action"] for c in SCENARIOS.values()}),
            "hint": "Gather evidence, choose the least risky verification and provide competing hypotheses."}


def grade(folder: Path) -> dict:
    rows, valid = read_events(folder)
    answers = json.loads(data_path(folder, "answers.json").read_text(encoding="utf-8"))
    if not isinstance(answers, dict):
        raise ValueError("Answers must be a JSON object")
    checks = {}
    for key, case in SCENARIOS.items():
        reply = answers.get(key, {})
        if not isinstance(reply, dict):
            reply = {}
        checks[key] = {
            "evidence_integrity": valid,
            "selections": {f: valid and reply.get(f) == case[f] for f in FIELDS},
            "reasoning_length_only": len(str(reply.get("reasoning") or "").strip()) >= 200,
            "counterargument": case["counter"]
        }
    points = sum(sum(x["selections"].values()) for x in checks.values())
    return {"score": points, "maximum": 12,
            "pass_objective": valid and points >= 10,
            "events_loaded": len(rows),
            "cases": checks,
            "notice": "Written reasoning is checked for length only; a reviewer must evaluate accuracy."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("init", "analyze", "options", "grade"))
    p.add_argument("--workspace", default="academy-batch11")
    p.add_argument("--case", choices=tuple(SCENARIOS), default="release_regression")
    args = p.parse_args(argv)
    try:
        if args.command == "init":
            initialize(canonical(args.workspace))
        else:
            folder = canonical(args.workspace)
            result = (analyze(folder) if args.command == "analyze"
                      else options(args.case) if args.command == "options"
                      else grade(folder))
            print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, KeyError, json.JSONDecodeError) as exc:
        print("Batch 11 error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
