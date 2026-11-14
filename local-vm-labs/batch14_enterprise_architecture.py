#!/usr/bin/env python3
"""Batch 14 — offline enterprise identity and segmentation defense simulator.

Uses fictional graph nodes, access decisions and detection events only.
No sockets, real identities, scanning, exploitation or OS configuration changes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

NODES = ("contractor", "employee", "helpdesk", "app", "finance", "admin")
EDGES = (
    ("contractor", "app", "web_access"),
    ("employee", "app", "web_access"),
    ("helpdesk", "admin", "privileged_access"),
    ("app", "finance", "service_read"),
)
SCENARIOS = {
    "excessive_role": {
        "situation": "Fictional helpdesk role has unrestricted administrative access.",
        "expected": "deny_helpdesk_admin",
        "monitor": "privileged_access_denied",
        "reason": "Least privilege limits privileged operations to approved principals."
    },
    "lateral_path": {
        "situation": "Application workload can reach finance records without service authorization.",
        "expected": "deny_app_finance",
        "monitor": "cross_zone_service_denied",
        "reason": "Segmentation and workload authorization should restrict cross-zone access."
    },
    "contractor_scope": {
        "situation": "Contractor's web access must not become finance or administrative access.",
        "expected": "restrict_contractor",
        "monitor": "contractor_boundary_denied",
        "reason": "Identity and network location are not substitutes for resource authorization."
    },
    "valid_employee": {
        "situation": "A legitimate employee must still reach the application after hardening.",
        "expected": "retain_employee_access",
        "monitor": "normal_business_allowed",
        "reason": "Negative tests alone may hide a business-breaking deny-all rule."
    }
}
CONTROLS = ("deny_helpdesk_admin", "deny_app_finance", "restrict_contractor", "retain_employee_access")
EVENTS = ("privileged_access_denied", "cross_zone_service_denied", "contractor_boundary_denied", "normal_business_allowed")


def folder_path(raw: str) -> Path:
    path = Path(raw).expanduser().absolute()
    if path == Path(path.anchor) or not path.name or any(p.is_symlink() for p in (path, *p.parents)):
        raise ValueError("Refusing root or symlinked workspace")
    return path


def state_path(folder: Path) -> Path:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize fresh training workspace first")
    path = folder / "policy.json"
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 8192:
        raise ValueError("Missing or unsafe policy.json")
    return path


def read_state(folder: Path) -> dict:
    state = json.loads(state_path(folder).read_text(encoding="utf-8"))
    if not isinstance(state, dict) or set(state) != {"enabled", "observations"}:
        raise ValueError("Unexpected policy structure")
    if not isinstance(state["enabled"], list) or any(x not in CONTROLS for x in state["enabled"]):
        raise ValueError("Unknown control")
    if not isinstance(state["observations"], list) or any(x not in EVENTS for x in state["observations"]):
        raise ValueError("Unknown event")
    return state


def save_state(folder: Path, state: dict) -> None:
    state_path(folder).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def initialize(folder: Path) -> None:
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():
        raise ValueError("Refusing to overwrite existing workspace")
    folder.mkdir(mode=0o700)
    (folder / "policy.json").write_text(json.dumps({"enabled": [], "observations": []}, indent=2) + "\n", encoding="utf-8")
    print("Created disposable fictional policy workspace; initial controls deliberately missing.")


def observe(state: dict) -> dict:
    enabled = set(state["enabled"])
    access = {
        "helpdesk_to_admin": "deny" if "deny_helpdesk_admin" in enabled else "allow",
        "app_to_finance": "deny" if "deny_app_finance" in enabled else "allow",
        "contractor_to_app": "limited" if "restrict_contractor" in enabled else "unrestricted",
        "employee_to_app": "allow" if "retain_employee_access" in enabled else "deny",
    }
    return {"nodes": list(NODES), "fictional_edges": list(EDGES),
            "access": access, "detections_recorded": state["observations"],
            "note": "This is a deterministic policy model, not real traffic or production authorization."}


def enable(folder: Path, control: str) -> None:
    if control not in CONTROLS:
        raise ValueError("Unsupported control")
    state = read_state(folder)
    if control not in state["enabled"]:
        state["enabled"].append(control)
    save_state(folder, state)
    print("Training control enabled:", control)


def detect(folder: Path, event: str) -> None:
    if event not in EVENTS:
        raise ValueError("Unsupported detection evidence")
    state = read_state(folder)
    if event not in state["observations"]:
        state["observations"].append(event)
    save_state(folder, state)
    print("Simulated detection recorded:", event)


def grade(folder: Path) -> dict:
    state = read_state(folder)
    access = observe(state)["access"]
    controls = {
        "admin_least_privilege": access["helpdesk_to_admin"] == "deny",
        "finance_segmented": access["app_to_finance"] == "deny",
        "contractor_scope_limited": access["contractor_to_app"] == "limited",
        "employee_positive_access": access["employee_to_app"] == "allow",
    }
    events = {
        "privileged_denial_logged": "privileged_access_denied" in state["observations"] and controls["admin_least_privilege"],
        "cross_zone_denial_logged": "cross_zone_service_denied" in state["observations"] and controls["finance_segmented"],
        "contractor_boundary_logged": "contractor_boundary_denied" in state["observations"] and controls["contractor_scope_limited"],
        "legitimate_access_logged": "normal_business_allowed" in state["observations"] and controls["employee_positive_access"],
    }
    checks = {**controls, **events}
    score = sum(checks.values())
    return {"score": score, "maximum": 8, "objective_pass": score == 8, "checks": checks,
            "notice": "A perfect score demonstrates only configuration of fictional policy; the source exposes the controls and cannot certify real-world skill."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("init", "inspect", "controls", "enable", "record", "grade"))
    p.add_argument("--workspace", default="academy-batch14")
    p.add_argument("--control", choices=CONTROLS)
    p.add_argument("--event", choices=EVENTS)
    args = p.parse_args(argv)
    try:
        folder = folder_path(args.workspace)
        if args.action == "init":
            initialize(folder)
        elif args.action == "controls":
            print(json.dumps({"controls": CONTROLS, "events": EVENTS, "scenarios": SCENARIOS}, indent=2))
        elif args.action == "inspect":
            print(json.dumps(observe(read_state(folder)), indent=2))
        elif args.action == "enable":
            if not args.control:
                p.error("enable requires --control")
            enable(folder, args.control)
        elif args.action == "record":
            if not args.event:
                p.error("record requires --event")
            detect(folder, args.event)
        else:
            print(json.dumps(grade(folder), indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        print("Batch 14 error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
