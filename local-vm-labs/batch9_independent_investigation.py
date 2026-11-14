#!/usr/bin/env python3
"""Batch 9: offline, synthetic incident investigation with objective checks.

No sockets, subprocesses, administrator permissions, credentials, external
targets, system changes, or access to Academy progress. Python standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

CASES = {
    "windows": {
        "title": "Windows: change correlation versus credential compromise",
        "evidence": [
            "14:00Z approved deployment CHG-204 began on APP-TRAINING.",
            "14:02Z two failed login events for a fictional user.",
            "14:05Z same user successfully signed in from their expected workstation.",
            "14:07Z training application reports configuration path missing.",
            "14:08Z application health endpoint returned 503."
        ],
        "diagnoses": ["configuration_regression", "credential_compromise", "dns_failure"],
        "actions": ["restore_approved_configuration", "disable_antivirus", "reset_every_account"],
        "tests": ["health_and_approved_transaction", "count_failed_logins", "verify_service_name_only"],
        "answer": ["configuration_regression", "restore_approved_configuration", "health_and_approved_transaction"],
        "why": "The approved change and missing path support a configuration regression; failures alone do not establish a breach."
    },
    "linux": {
        "title": "Linux: directory traversal and service identity",
        "evidence": [
            "Service runs as svc-reports and must read /training/public.",
            "The parent training directory is owned by root with mode 0700.",
            "Report file itself has mode 0640 and expected reader group.",
            "Service journal shows Permission denied traversing parent.",
            "An operator proposes chmod -R 777 /training."
        ],
        "diagnoses": ["directory_traversal_denied", "dns_failure", "cpu_overload"],
        "actions": ["approved_minimal_traverse_acl", "recursive_world_write", "disable_audit_logs"],
        "tests": ["authorized_read_and_unauthorized_denial", "service_process_exists", "ping_external_host"],
        "answer": ["directory_traversal_denied", "approved_minimal_traverse_acl", "authorized_read_and_unauthorized_denial"],
        "why": "A directory needs traverse permission to access a child; scoped permission plus a denied negative test is preferable."
    },
    "network": {
        "title": "Network: DNS versus transport versus application",
        "evidence": [
            "A fictional client reports portal.training.example did not resolve.",
            "The local mock resolver returned NXDOMAIN for portal.training.example.",
            "A direct connection to the fictional training service's documented address succeeds.",
            "The service responds with HTTP 200 to its public health endpoint.",
            "No evidence of malicious DNS redirection is provided."
        ],
        "diagnoses": ["missing_training_dns_record", "service_down", "host_compromised"],
        "actions": ["correct_approved_dns_record", "disable_firewall_globally", "scan_public_network"],
        "tests": ["resolver_then_http_health", "check_process_name", "repeat_unrelated_ping"],
        "answer": ["missing_training_dns_record", "correct_approved_dns_record", "resolver_then_http_health"],
        "why": "A name failure with working address-level service supports a DNS-record problem, not a confirmed compromise."
    },
    "web": {
        "title": "Web: cross-tenant authorization control",
        "evidence": [
            "Two invented tenants, A and B, have separately owned report IDs.",
            "Tenant A requests B's report through a fictional training fixture.",
            "The mock server returns 200 and report data to A.",
            "The browser normally hides B's link from A.",
            "Response headers include X-Content-Type-Options: nosniff."
        ],
        "diagnoses": ["missing_object_authorization", "dns_failure", "missing_security_header"],
        "actions": ["enforce_server_side_owner_check", "hide_link_only", "remove_access_logs"],
        "tests": ["same_tenant_allow_cross_tenant_deny", "homepage_returns_200", "browser_menu_hidden"],
        "answer": ["missing_object_authorization", "enforce_server_side_owner_check", "same_tenant_allow_cross_tenant_deny"],
        "why": "UI hiding and security headers are not substitutes for server-side per-object authorization."
    },
    "cloud": {
        "title": "Cloud: offboarding and stale sessions",
        "evidence": [
            "A fictional employee was disabled at 09:00Z.",
            "Password authentication now fails, as intended.",
            "A previously issued mock access token still reads a protected report.",
            "The application has no token-revocation event in the mock record.",
            "No real credentials, cloud services or tenants are involved."
        ],
        "diagnoses": ["unrevoked_existing_token", "database_corruption", "dns_failure"],
        "actions": ["revoke_sessions_and_bound_token_lifetime", "delete_all_audit_events", "make_reports_public"],
        "tests": ["old_token_deny_new_authorized_allow", "login_page_responds", "user_record_disabled"],
        "answer": ["unrevoked_existing_token", "revoke_sessions_and_bound_token_lifetime", "old_token_deny_new_authorized_allow"],
        "why": "Disabling a login does not always invalidate already-issued tokens; negative checks must test the old token."
    }
}
FIELDS = ("diagnosis", "action", "verification")

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def workspace_from(value: str) -> Path:
    path = Path(value).expanduser().absolute()
    if path.exists() and path.is_symlink():
        raise ValueError("Refusing a symlink workspace")
    return path

def initialize(workspace: Path) -> None:
    # Atomic creation prevents overwriting any existing user directory.
    workspace.mkdir(parents=False, exist_ok=False)
    for key, case in CASES.items():
        evidence = "\n".join(f"{i+1}. {line}" for i, line in enumerate(case["evidence"])) + "\n"
        (workspace / (key + ".txt")).write_text(evidence, encoding="utf-8")
    template = {
        key: {"diagnosis": "", "action": "", "verification": "", "reasoning": ""}
        for key in CASES
    }
    (workspace / "answers.json").write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
    manifest = {key: digest(workspace / (key + ".txt")) for key in CASES}
    (workspace / "evidence_sha256.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Created {workspace}; edit answers.json after reading each fictional evidence file.")
    print("Use 'inspect' for allowed answer choices; 'grade' checks 15 objective selections.")

def inspection(case_id: str) -> None:
    case = CASES[case_id]
    print(case_id.upper() + " — " + case["title"])
    for field, options_key in (("diagnosis", "diagnoses"), ("action", "actions"), ("verification", "tests")):
        print(field + ": " + " | ".join(case[options_key]))

def grade(workspace: Path) -> dict:
    answers_file = workspace / "answers.json"
    answers = json.loads(answers_file.read_text(encoding="utf-8"))
    manifest = json.loads((workspace / "evidence_sha256.json").read_text(encoding="utf-8"))
    results = {}
    total = 0
    for key, case in CASES.items():
        intact = (key + ".txt" in manifest and
                  digest(workspace / (key + ".txt")) == manifest[key + ".txt"])
        selected = answers.get(key, {})
        if not isinstance(selected, dict):
            selected = {}
        checks = {
            field: selected.get(field) == expected
            for field, expected in zip(FIELDS, case["answer"])
        }
        if not intact:
            checks = {field: False for field in FIELDS}
        points = sum(checks.values())
        total += points
        results[key] = {
            "evidence_intact": intact,
            "objective_points": points,
            "checks": checks,
            "reasoning_present_not_graded": len(str(selected.get("reasoning", "")).strip()) >= 150,
            "feedback": case["why"] if points < 3 else "Objective selections correct; written reasoning needs human review."
        }
    return {
        "score": total, "maximum": len(CASES)*3, "pass_objective": total >= 12,
        "cases": results,
        "warning": "Offline synthetic selections only. No automated assessment of writing or real-machine competency."
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "inspect", "grade"])
    parser.add_argument("--workspace", default="academy-batch9-work")
    parser.add_argument("--case", choices=list(CASES), default="windows")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        path = workspace_from(args.workspace)
        if args.command == "init":
            initialize(path)
        elif args.command == "inspect":
            inspection(args.case)
            print((path / (args.case + ".txt")).read_text(encoding="utf-8"))
        else:
            result = grade(path)
            print(json.dumps(result, indent=2) if args.json else
                  f"Objective score: {result['score']}/{result['maximum']}\n" +
                  "\n".join(f"{key}: {value['objective_points']}/3 — {value['feedback']}"
                            for key, value in result["cases"].items()))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("Batch 9 error: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
