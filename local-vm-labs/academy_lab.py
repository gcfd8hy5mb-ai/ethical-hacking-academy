#!/usr/bin/env python3
"""Ethical Hacking Academy: real, offline Linux practice inside a user-owned VM.

No root access, inbound server, scanning, external network, or third-party targets.
This exercise intentionally runs with the logged-in learner's permissions.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
from datetime import datetime, timezone

BASE = Path.home() / "academy-local-lab"
VERSION = 1


def files() -> dict[str, Path]:
    return {
        "permissions": BASE / "permissions" / "report.txt",
        "logs": BASE / "logs" / "resolver.log",
        "finding": BASE / "logs" / "finding.txt",
        "config": BASE / "config" / "web.conf",
        "evidence": BASE / "evidence.json",
    }


def setup() -> None:
    if BASE.exists():
        raise SystemExit(f"Lab already exists: {BASE}. Use 'reset' only if you intend to replace it.")
    f = files()
    for name in ("permissions", "logs", "config"):
        (BASE / name).mkdir(parents=True)
    f["permissions"].write_text(
        "TRAINING REPORT\nOwner: lab-student\nOnly authorized learners should read this file.\n",
        encoding="utf-8",
    )
    os.chmod(f["permissions"], 0o600)
    f["logs"].write_text(
        "2026-11-07T09:00:00Z INFO resolver started\n"
        "2026-11-07T09:01:00Z ERROR dns timeout querying app.lab.example\n"
        "2026-11-07T09:01:05Z ERROR dns timeout querying app.lab.example\n"
        "2026-11-07T09:02:00Z INFO network interface up\n",
        encoding="utf-8",
    )
    f["config"].write_text(
        "server {\n    listen 80 extra;\n    server_name app.lab.example;\n}\n",
        encoding="utf-8",
    )
    print(f"Offline Linux exercises created at {BASE}")
    print("Run 'python3 academy_lab.py status' to see your three missions.")


def check_state() -> dict:
    f = files()
    if not BASE.is_dir():
        raise SystemExit("Lab not initialized. Run 'python3 academy_lab.py setup'.")
    # Check user-created artifacts on this VM only; never inspect other systems.
    permission_ok = (
        f["permissions"].is_file()
        and stat.S_IMODE(f["permissions"].stat().st_mode) == 0o640
    )
    findings = f["finding"].read_text(encoding="utf-8", errors="replace").lower() if f["finding"].is_file() else ""
    logs_ok = "dns" in findings and "timeout" in findings and len(findings.strip()) >= 45
    config_text = f["config"].read_text(encoding="utf-8", errors="replace") if f["config"].is_file() else ""
    config_ok = "listen 80;" in config_text and "listen 80 extra;" not in config_text
    return {
        "permissions": permission_ok,
        "log_analysis": logs_ok,
        "config_repair": config_ok,
    }


def status() -> None:
    checks = check_state()
    print(f"Lab: {BASE}")
    print("Mission 1 — Linux permissions: chmod 640 permissions/report.txt")
    print("Mission 2 — Investigate logs/resolver.log and write logs/finding.txt")
    print("          Describe the DNS timeout, what the log does and does not prove.")
    print("Mission 3 — Repair config/web.conf so the directive reads: listen 80;")
    print("          No web service is installed or started by this exercise.")
    print()
    for name, passed in checks.items():
        print(f"{name:15} {'PASS' if passed else 'INCOMPLETE'}")
    print("Use 'python3 academy_lab.py check' for local, deterministic validation.")


def check() -> None:
    results = check_state()
    for name, passed in results.items():
        print(f"{name}: {'PASS' if passed else 'NOT YET'}")
    if all(results.values()):
        print("TRAIN{OFFLINE_LINUX_MISSIONS_COMPLETE}")
        print("This confirms file-state checks, not practical competence or independent grading.")
    else:
        print("Inspect the files, correct outstanding issues and rerun this command.")


def export() -> None:
    results = check_state()
    f = files()
    payload = {
        "schema": "eh-local-linux-evidence-v1",
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "lab_version": VERSION,
        "checks": results,
        "limitation": "Learner-generated self-evidence; not proof of independent assessment.",
        "finding": f["finding"].read_text(encoding="utf-8", errors="replace")[:5000]
        if f["finding"].is_file() else "",
    }
    f["evidence"].write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Exported: {f['evidence']}")


def reset() -> None:
    if not BASE.is_dir() or BASE.is_symlink():
        raise SystemExit("Lab folder absent or not a normal directory. Nothing changed.")
    confirm = input(f"Delete ONLY {BASE} and recreate exercise files? Type RESET: ")
    if confirm != "RESET":
        print("Reset cancelled.")
        return
    # Explicitly scoped to our known lab directory in the current user's home.
    shutil.rmtree(BASE)
    setup()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "status", "check", "export", "reset"))
    args = parser.parse_args()
    {"setup": setup, "status": status, "check": check, "export": export, "reset": reset}[args.action]()


if __name__ == "__main__":
    main()
