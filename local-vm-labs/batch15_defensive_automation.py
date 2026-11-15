#!/usr/bin/env python3
"""Batch 15: offline defensive vulnerability-management and control validation.

Generates fictional asset inventory, evaluates prioritization and remediation,
and checks positive/negative test selections. No network calls or OS changes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

CASES = {
 "workstation": {
  "asset": "Training Windows endpoint W-101",
  "facts": ["An approved update is pending", "The endpoint is used by normal staff",
            "No exploitation or malicious activity confirmed"],
  "decision": "schedule_approved_patch_with_rollback",
  "validation": "check_version_and_normal_signin",
  "priority": "medium",
  "alternate": "Asset importance and patch exposure could change urgency."
 },
 "linux_service": {
  "asset": "Training Linux report service L-202",
  "facts": ["Service principal cannot traverse a required parent directory",
            "A technician suggests recursively world-writable permissions",
            "No production operating system is accessed"],
  "decision": "review_narrow_acl_for_service_identity",
  "validation": "approved_report_allow_private_report_deny",
  "priority": "medium",
  "alternate": "Service-account mismatch is another possible contributor."
 },
 "web_access": {
  "asset": "Fictional multitenant web API A-303",
  "facts": ["Tenant A mock user reads Tenant B's record",
            "Frontend normally hides other tenant links",
            "Finding exists only in the synthetic exercise"],
  "decision": "enforce_resource_ownership_on_server",
  "validation": "same_tenant_allow_cross_tenant_deny",
  "priority": "high",
  "alternate": "Production exploitability cannot be inferred from a fictional case."
 },
 "recovery": {
  "asset": "Fictional recovery system B-404",
  "facts": ["Backup job marked complete", "Integrity check does not match",
            "No isolated test restore was recorded"],
  "decision": "preserve_and_validate_backup_before_restore",
  "validation": "isolated_restore_integrity_and_access_checks",
  "priority": "high",
  "alternate": "A digest mismatch alone does not identify its cause."
 }
}
FIELDS = ("decision", "validation", "priority")

def safe_workspace(raw: str) -> Path:
    p = Path(raw).expanduser().absolute()
    if p == Path(p.anchor) or not p.name or any(x.is_symlink() for x in (p, *p.parents)):
        raise ValueError("Refuse filesystem root or symlinked workspace")
    return p

def checked_file(folder: Path, name: str) -> Path:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize a new disposable workspace")
    p = folder / name
    if not p.is_file() or p.is_symlink() or p.stat().st_size > 100_000:
        raise ValueError("Missing or unsafe training file: " + name)
    return p

def initialize(folder: Path) -> None:
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():
        raise ValueError("Refusing to overwrite existing workspace")
    folder.mkdir(mode=0o700)
    evidence = {k: {"asset": v["asset"], "facts": v["facts"]} for k,v in CASES.items()}
    body = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    (folder / "inventory.json").write_text(body, encoding="utf-8")
    manifest = {"inventory_sha256": hashlib.sha256(body.encode()).hexdigest()}
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    answers = {k: {**{field: "" for field in FIELDS}, "reasoning": ""} for k in CASES}
    (folder / "answers.json").write_text(json.dumps(answers, indent=2) + "\n", encoding="utf-8")
    print("Created four synthetic assets, evidence manifest and blank answer template.")

def inspect(folder: Path) -> tuple[dict, bool]:
    raw = checked_file(folder, "inventory.json").read_bytes()
    manifest = json.loads(checked_file(folder, "manifest.json").read_text(encoding="utf-8"))
    evidence = json.loads(raw)
    if not isinstance(manifest, dict) or not isinstance(evidence, dict) or set(evidence) != set(CASES):
        raise ValueError("Invalid training inventory structure")
    return evidence, manifest.get("inventory_sha256") == hashlib.sha256(raw).hexdigest()

def options() -> dict:
    return {f: sorted({case[f] for case in CASES.values()}) for f in FIELDS}

def grade(folder: Path) -> dict:
    _, intact = inspect(folder)
    answers = json.loads(checked_file(folder,"answers.json").read_text(encoding="utf-8"))
    if not isinstance(answers, dict):
        raise ValueError("Answers must be a JSON object")
    scored = {}
    for key, case in CASES.items():
        entry = answers.get(key, {})
        if not isinstance(entry, dict):
            entry = {}
        checks = {f: bool(intact and entry.get(f) == case[f]) for f in FIELDS}
        scored[key] = {
            "points": sum(checks.values()), "checks": checks,
            "written_reasoning_present_not_graded": len(str(entry.get("reasoning") or "").strip()) >= 200,
            "important_limit": case["alternate"]
        }
    total = sum(v["points"] for v in scored.values())
    return {"score": total, "maximum": 12, "objective_pass": intact and total >= 10,
            "evidence_integrity": intact, "cases": scored,
            "warning": "Synthetic offline answers only; written reasoning and real practical ability not graded."}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "inspect", "options", "grade"))
    parser.add_argument("--workspace", default="academy-batch15")
    args = parser.parse_args(argv)
    try:
        folder = safe_workspace(args.workspace)
        if args.command == "init":
            initialize(folder)
        elif args.command == "inspect":
            evidence, intact = inspect(folder)
            print(json.dumps({"inventory": evidence, "intact": intact}, indent=2))
        elif args.command == "options":
            print(json.dumps(options(), indent=2))
        else:
            print(json.dumps(grade(folder), indent=2))
        return 0
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print("Batch 15 error: " + str(error), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
