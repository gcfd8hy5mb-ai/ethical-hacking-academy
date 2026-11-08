#!/usr/bin/env python3
"""Read-only evidence review for the Academy's own offline Linux practice files.

Designed for WSL 1 or an Ubuntu VM. No root, scanning, inbound ports, network
requests, subprocesses, shell execution, or changes to the learner's files.
The result is a repeatable file-evidence review, not a competency certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
from datetime import datetime, timezone
from pathlib import Path

BASE = Path.home() / "academy-local-lab"
REQUIRED = ("permissions/report.txt", "logs/resolver.log",
            "logs/finding.txt", "config/web.conf")


def safe_text(relative: str) -> tuple[str | None, str | None, dict]:
    """Read only regular files inside a non-symlinked, learner-owned lab tree."""
    node = BASE
    if not BASE.exists() or BASE.is_symlink() or not BASE.is_dir():
        return None, "Lab directory missing, symlinked or invalid", {}
    for part in Path(relative).parts:
        if part in ("", ".", "..") or part.startswith("/"):
            return None, "Unsafe path component", {}
        node = node / part
        if node.is_symlink():
            return None, "Symlinked path refused", {}
    if not node.is_file():
        return None, "Required regular file is missing", {}
    try:
        raw = node.read_bytes()
        if len(raw) > 32_768:
            return None, "Evidence file exceeds 32 KiB limit", {}
        decoded = raw.decode("utf-8")
        mode = stat.S_IMODE(node.stat().st_mode)
        return decoded, None, {
            "mode": oct(mode),
            "size_bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()
        }
    except (OSError, UnicodeError, ValueError) as error:
        return None, "File cannot be read as UTF-8: " + type(error).__name__, {}


def evaluate() -> dict:
    report = {
        "schema": "eh-offline-evidence-review-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "lab_relative": "academy-local-lab",
        "checks": {},
        "artifacts": {},
        "review_questions": [
            "Does the observation prove a security incident, or only a DNS timeout?",
            "Which corroborating evidence would distinguish resolver failure from upstream failure?",
            "Was any real network service started? If not, what cannot be inferred from the config edit?"
        ],
        "limitations": [
            "Checks local file metadata and a constrained training fixture only.",
            "Text headings and file-state checks do not establish reasoning quality.",
            "The original offline exercise is not independently proctored or accredited."
        ]
    }
    texts = {}
    for name in REQUIRED:
        content, error, metadata = safe_text(name)
        texts[name] = content
        report["artifacts"][name] = {"error": error, **metadata}

    perm = report["artifacts"]["permissions/report.txt"]
    report["checks"]["permissions_mode_0640"] = perm.get("mode") == "0o640"

    log = texts["logs/resolver.log"] or ""
    report["checks"]["synthetic_dns_log_present"] = (
        "ERROR dns timeout querying app.lab.example" in log
        and log.count("ERROR dns timeout") >= 2
    )

    finding = texts["logs/finding.txt"] or ""
    upper = finding.upper()
    report["checks"]["finding_has_observation_section"] = "OBSERVED:" in upper
    report["checks"]["finding_has_uncertainty_section"] = "UNKNOWN:" in upper
    report["checks"]["finding_has_next_step_section"] = "NEXT STEP:" in upper
    report["checks"]["finding_mentions_dns_and_timeout"] = (
        "dns" in finding.lower() and "timeout" in finding.lower()
    )

    config = texts["config/web.conf"] or ""
    lines = [line.strip() for line in config.splitlines()]
    report["checks"]["config_single_correct_listen_directive"] = (
        lines.count("listen 80;") == 1
        and not any("listen 80 extra;" in line for line in lines)
    )
    report["checks"]["all_required_files_readable"] = all(
        report["artifacts"][name]["error"] is None for name in REQUIRED
    )
    report["file_check_pass"] = all(report["checks"].values())
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true",
                        help="Output a machine-readable evidence-review report.")
    args = parser.parse_args()
    data = evaluate()
    if args.json:
        print(json.dumps(data, indent=2))
        return
    print("Academy Offline Linux Evidence Review (read only)")
    print("No changes made; no ports or network services started.\n")
    for name, passed in data["checks"].items():
        print(("PASS " if passed else "REVIEW ") + name)
    if data["file_check_pass"]:
        print("\nAll file-state and structured-note checks passed.")
    else:
        print("\nOne or more checks need attention. Revisit the local lab files.")
    print("Passing does not constitute independent technical or academic assessment.")
    for prompt in data["review_questions"]:
        print("- " + prompt)


if __name__ == "__main__":
    main()
