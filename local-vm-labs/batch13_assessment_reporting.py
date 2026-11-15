#!/usr/bin/env python3
"""Batch 13: offline authorized assessment and vulnerability reporting simulator.

Uses only fictional JSON training data and an allowlisted disposable workspace.
No network access, vulnerability probes, exploits or real credentials.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

CASES = {
 "tenant_isolation": {
  "scope": "Fictional tenant-report application; tabletop assessment only",
  "evidence": ["Tenant A user received tenant B's mock report with HTTP 200",
               "Client interface normally hides cross-tenant report identifiers",
               "No production customers, tokens or network requests used"],
  "finding": "object_authorization_missing",
  "validation": "test_cross_tenant_denial_and_same_tenant_allow",
  "remediation": "enforce_object_owner_server_side",
  "priority": "high",
  "caveat": "A browser-hidden link is not server authorization; synthetic status does not prove real-world exposure."
 },
 "session_lifecycle": {
  "scope": "Fictional training identity system; no real account usage",
  "evidence": ["Mock disabled user cannot start a new login",
               "Earlier mock session continues to access fictional private data",
               "No revocation record supplied"],
  "finding": "previous_session_remains_valid",
  "validation": "deny_old_session_and_allow_current_user",
  "remediation": "invalidate_sessions_and_enforce_entitlement",
  "priority": "high",
  "caveat": "New login denial alone cannot prove that older sessions have been revoked."
 },
 "configuration_drift": {
  "scope": "Locally modeled service configuration; read-only analysis",
  "evidence": ["Approved change alters mock report endpoint configuration",
               "Health remains 200 while report body contains stale data",
               "Deployment record is available but root cause unconfirmed"],
  "finding": "data_integrity_regression",
  "validation": "compare_expected_data_after_approved_rollback",
  "remediation": "restore_reviewed_configuration_and_retest",
  "priority": "medium",
  "caveat": "An HTTP 200 is not proof that its response data are accurate."
 },
 "backup_controls": {
  "scope": "Fictional backup and restore records; no production restoration",
  "evidence": ["Backup job reported completion", "Integrity validation for the backup failed",
               "No independent isolated restore has been completed"],
  "finding": "restore_readiness_unverified",
  "validation": "verify_integrity_and_restore_isolated_copy",
  "remediation": "hold_unverified_backup_and_validate_recovery",
  "priority": "high",
  "caveat": "Backup existence does not establish integrity or restorability."
 }
}
FIELDS = ("finding","validation","remediation","priority")

def checked_workspace(raw):
    path=Path(raw).expanduser().absolute()
    if path==Path(path.anchor) or not path.name or any(p.is_symlink() for p in (path,*path.parents)):
        raise ValueError("Refuse root and symlinked workspace paths")
    return path

def fixture(folder,name):
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize a new disposable workspace first")
    file=folder/name
    if file.is_symlink() or not file.is_file() or file.stat().st_size>100000:
        raise ValueError("Missing or unsafe fixture file")
    return file

def init(folder):
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():
        raise ValueError("Refusing to overwrite or create outside existing parent")
    folder.mkdir(mode=0o700)
    records={key:{"scope":c["scope"],"evidence":c["evidence"]} for key,c in CASES.items()}
    raw=json.dumps(records,sort_keys=True,indent=2)+"\n"
    (folder/"evidence.json").write_text(raw,encoding="utf-8")
    (folder/"manifest.json").write_text(json.dumps({"sha256":hashlib.sha256(raw.encode()).hexdigest()},indent=2)+"\n",encoding="utf-8")
    answers={key:{**{field:"" for field in FIELDS},"reasoning":"","out_of_scope":""} for key in CASES}
    (folder/"answers.json").write_text(json.dumps(answers,indent=2)+"\n",encoding="utf-8")
    print("Four fictional assessment cases initialized. Read evidence and edit answers.json.")

def read_evidence(folder):
    raw=fixture(folder,"evidence.json").read_bytes()
    record=json.loads(raw)
    manifest=json.loads(fixture(folder,"manifest.json").read_text(encoding="utf-8"))
    if not isinstance(record,dict) or set(record)!=set(CASES) or not isinstance(manifest,dict):
        raise ValueError("Invalid fixture structure")
    return record,manifest.get("sha256")==hashlib.sha256(raw).hexdigest()

def options():
    return {field:sorted({case[field] for case in CASES.values()}) for field in FIELDS}

def assess(folder):
    evidence,intact=read_evidence(folder)
    answers=json.loads(fixture(folder,"answers.json").read_text(encoding="utf-8"))
    if not isinstance(answers,dict):
        raise ValueError("Answer structure must be a JSON object")
    detail={}
    for key,correct in CASES.items():
        selected=answers.get(key,{})
        if not isinstance(selected,dict): selected={}
        checks={field:bool(intact and selected.get(field)==correct[field]) for field in FIELDS}
        detail[key]={"objective_checks":checks,"points":sum(checks.values()),
                     "written_reasoning_present_not_graded":len(str(selected.get("reasoning") or "").strip())>=200,
                     "out_of_scope_statement_present_not_graded":len(str(selected.get("out_of_scope") or "").strip())>=40,
                     "explanation":correct["caveat"]}
    score=sum(item["points"] for item in detail.values())
    return {"score":score,"maximum":16,"objective_pass":score>=13 and intact,
            "evidence_integrity":intact,"cases":detail,
            "limitations":"Fictional evidence, no active testing; written quality requires independent review."}

def report(folder):
    result=assess(folder)
    lines=["# Fictional Authorized Security Assessment", "",
           "Scope: Offline training evidence only; no real hosts, accounts, networks or exploits.", "",
           f"Objective answer score: {result['score']}/16 (not a professional qualification).", ""]
    for key,item in result["cases"].items():
        case=CASES[key]
        lines.extend([f"## {key.replace('_',' ').title()}",
                      "Observed synthetic evidence:",
                      *("- "+event for event in case["evidence"]),
                      "Analyst reasoning and action require review. "+case["caveat"],
                      f"Objective selections correct: {item['points']}/4.", ""])
    lines.extend(["## Reviewer checklist", "- Written authorization and test scope",
                  "- Provenance, missing evidence, alternatives",
                  "- Severity justified by impact and context",
                  "- Least privilege remediation and rollback",
                  "- Positive and negative post-remediation tests",
                  "- Report limitations and executive communication"])
    return "\n".join(lines)+"\n"

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=("init","inspect","options","grade","report"))
    p.add_argument("--workspace",default="academy-batch13")
    args=p.parse_args(argv)
    try:
        folder=checked_workspace(args.workspace)
        if args.command=="init": init(folder)
        elif args.command=="inspect":
            evidence,intact=read_evidence(folder)
            print(json.dumps({"evidence":evidence,"integrity_matches_manifest":intact},indent=2))
        elif args.command=="options": print(json.dumps(options(),indent=2))
        elif args.command=="grade": print(json.dumps(assess(folder),indent=2))
        else: print(report(folder))
        return 0
    except (ValueError,TypeError,OSError,UnicodeError,json.JSONDecodeError) as exc:
        print("Batch 13 error: "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
