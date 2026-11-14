#!/usr/bin/env python3
"""Batch 12: entirely inert forensics, artifact triage, containment and recovery.

Only fictional text and JSON evidence. Does not execute or download unknown
programs, inspect real OS data, access networks, or change Academy progress.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

CASES = {
 "suspicious_attachment": {
  "artifact": "Fictional invoice note: URGENT enable macros to see payment details. This is text, not a document.",
  "observations": ["Unexpected attachment claimed to be an invoice", "Message urges enabling macros", "No payload was executed and no endpoint log is available"],
  "diagnosis": "social_engineering_indicator",
  "contain": "quarantine_sample_and_check_mail_scope",
  "verify": "confirm_no_execution_and_document_uncertainty",
  "lesson": "Social-engineering markers warrant triage, not a claim of malicious execution."
 },
 "endpoint_alert": {
  "artifact": "Fictional EDR alert: script interpreter launched after a user action; signed update job also scheduled.",
  "observations": ["Execution alert with limited command context", "Signed enterprise maintenance task overlaps", "No process ancestry or file reputation included"],
  "diagnosis": "execution_needs_context",
  "contain": "preserve_telemetry_and_assess_isolation_impact",
  "verify": "correlate_process_tree_and_authorized_change",
  "lesson": "A process name alone cannot distinguish an authorized task from abuse."
 },
 "backup_recovery": {
  "artifact": "Fictional restore log: backup exists, but integrity validation failed before restore.",
  "observations": ["Recovery point is listed", "Backup verification reports a digest mismatch", "No successful test-restore record exists"],
  "diagnosis": "unverified_backup_integrity",
  "contain": "hold_restore_and_preserve_backup_copy",
  "verify": "validate_clean_restore_in_isolated_fixture",
  "lesson": "Backup presence does not establish recoverability or integrity."
 },
 "data_access": {
  "artifact": "Fictional report: departed employee token was accepted by a private-report training endpoint.",
  "observations": ["Password authentication disabled", "Earlier fictional session still accesses data", "No token revocation record is available"],
  "diagnosis": "stale_authorization_session",
  "contain": "revoke_fictional_sessions_without_global_lockout",
  "verify": "old_token_denied_valid_user_still_allowed",
  "lesson": "Offboarding must consider already-issued sessions and negative access tests."
 }
}
FIELDS = ("diagnosis","contain","verify")

def checked_folder(raw):
    p = Path(raw).expanduser().absolute()
    if p == Path(p.anchor) or not p.name or any(x.is_symlink() for x in (p, *p.parents)):
        raise ValueError("Use a non-root, non-symlinked workspace")
    return p

def safe_file(folder, name):
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize a fresh workspace first")
    p = folder / name
    if not p.is_file() or p.is_symlink() or p.stat().st_size > 100000:
        raise ValueError("Unsafe or missing fixture file: " + name)
    return p

def build(folder):
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():
        raise ValueError("Refusing to overwrite existing workspace")
    folder.mkdir(mode=0o700)
    source = {k:{"artifact":v["artifact"],"observations":v["observations"]} for k,v in CASES.items()}
    body = json.dumps(source, indent=2, sort_keys=True) + "\n"
    (folder / "evidence.json").write_text(body, encoding="utf-8")
    manifest = {"sha256": hashlib.sha256(body.encode()).hexdigest()}
    (folder / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    answers = {k:dict.fromkeys((*FIELDS,"reasoning"),"") for k in CASES}
    (folder / "answers.json").write_text(json.dumps(answers,indent=2)+"\n",encoding="utf-8")
    print("Created four fictional forensic cases and empty answer template.")

def inspect(folder):
    path = safe_file(folder,"evidence.json")
    raw = path.read_bytes()
    manifest = json.loads(safe_file(folder,"manifest.json").read_text(encoding="utf-8"))
    valid = isinstance(manifest,dict) and manifest.get("sha256")==hashlib.sha256(raw).hexdigest()
    evidence=json.loads(raw)
    if not isinstance(evidence,dict) or set(evidence)!=set(CASES):
        raise ValueError("Evidence structure changed")
    return evidence,valid

def choice_options():
    return {field:sorted({c[field] for c in CASES.values()}) for field in FIELDS}

def assess(folder):
    evidence, intact = inspect(folder)
    answers = json.loads(safe_file(folder,"answers.json").read_text(encoding="utf-8"))
    if not isinstance(answers,dict):
        raise ValueError("Answers must be an object")
    cases={}
    for key, expected in CASES.items():
        selected=answers.get(key,{})
        if not isinstance(selected,dict):
            selected={}
        checks={f: intact and selected.get(f)==expected[f] for f in FIELDS}
        cases[key]={"checks":checks,"score":sum(checks.values()),
                    "reasoning_length_only":len(str(selected.get("reasoning") or "").strip())>=200,
                    "explanation":expected["lesson"]}
    score=sum(v["score"] for v in cases.values())
    return {"score":score,"maximum":12,"objective_pass":intact and score>=10,
            "evidence_intact":intact,"cases":cases,
            "scope":"Synthetic inert artifacts only; no malware or real forensic evidence",
            "warning":"The editable source reveals answer keys; prose quality needs independent human review."}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("init","inspect","options","grade"))
    p.add_argument("--workspace",default="academy-batch12")
    args=p.parse_args(argv)
    try:
        folder=checked_folder(args.workspace)
        if args.command=="init":
            build(folder)
        elif args.command=="options":
            print(json.dumps(choice_options(),indent=2))
        elif args.command=="inspect":
            evidence,intact=inspect(folder)
            print(json.dumps({"evidence":evidence,"integrity_matches_manifest":intact},indent=2))
        else:
            print(json.dumps(assess(folder),indent=2))
        return 0
    except (ValueError,OSError,UnicodeError,TypeError,json.JSONDecodeError) as exc:
        print("Batch 12 lab error: "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
