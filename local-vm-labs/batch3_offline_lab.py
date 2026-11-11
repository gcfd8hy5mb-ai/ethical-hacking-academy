#!/usr/bin/env python3
"""Ethical Hacking Academy Batch 3: offline, standard-library practical lab.

Commands:
  python3 local-vm-labs/batch3_offline_lab.py init --workspace PATH
  python3 local-vm-labs/batch3_offline_lab.py check --workspace PATH
  python3 local-vm-labs/batch3_offline_lab.py check --workspace PATH --json
Works on Windows (py -3 instead of python3), macOS and Linux. No network activity,
no admin permissions, no subprocesses, no modifications outside the explicit
workspace. The setup refuses existing workspaces and symlinks. Results remain local.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path

FILES = {
    "events.csv": (
        "time,user,source,result\n"
        "2026-11-10T14:00:00Z,alex,192.0.2.10,success\n"
        "2026-11-10T14:01:00Z,blair,192.0.2.11,fail\n"
        "2026-11-10T14:02:00Z,blair,192.0.2.11,fail\n"
        "2026-11-10T14:03:00Z,casey,192.0.2.12,success\n"
    ),
    "permissions/private.txt": "Training-only example: not a real secret.\n",
    "config/service.txt": "hostname=academy.local\nlisten=127.0.0.1\nport=8080\n",
    "notes/investigation.txt": (
        "OBSERVED: two failed sign-ins for blair from 192.0.2.11.\n"
        "UNKNOWN: whether they were malicious or accidental.\n"
        "NEXT STEP: confirm MFA and session evidence from authorized logs.\n"
    ),
}
EXPECTED_COUNT = {"success": 2, "fail": 2}


def normal_workspace(value: str) -> Path:
    candidate = Path(value).expanduser().absolute()
    if not candidate.name or candidate == Path(candidate.anchor):
        raise ValueError("Refusing filesystem root as workspace")
    if candidate.is_symlink() or any(part.is_symlink() for part in candidate.parents):
        raise ValueError("Workspace path contains a symlink")
    return candidate


def init(workspace: Path) -> dict:
    if workspace.exists() or workspace.is_symlink():
        raise ValueError("Refusing to overwrite an existing workspace")
    if not workspace.parent.is_dir():
        raise ValueError("Choose a path under an existing parent directory")
    workspace.mkdir(mode=0o700)
    for name, content in FILES.items():
        target = workspace / name
        target.parent.mkdir(exist_ok=True)
        with target.open("x", encoding="utf-8", newline="") as stream:
            stream.write(content)
    return {"created": str(workspace), "files": list(FILES), "network_used": False}


def read_fixture(workspace: Path, relative: str) -> tuple[bytes | None, str | None]:
    node = workspace
    for part in Path(relative).parts:
        if part in ("", ".", ".."):
            return None, "unsafe path"
        node = node / part
        if node.is_symlink():
            return None, "symlink refused"
    if not node.is_file():
        return None, "missing file"
    try:
        if node.stat().st_size > 16_384:
            return None, "oversized file"
        return node.read_bytes(), None
    except OSError as error:
        return None, type(error).__name__


def check(workspace: Path) -> dict:
    checks = {}
    artifacts = {}
    if not workspace.is_dir() or workspace.is_symlink():
        return {"passed": False, "checks": {"workspace_exists": False},
                "limitations": ["The workspace is missing or a symlink."]}
    payloads = {}
    for name in FILES:
        raw, error = read_fixture(workspace, name)
        payloads[name] = raw
        artifacts[name] = ({"error": error} if error else
                           {"sha256": hashlib.sha256(raw).hexdigest(),
                            "bytes": len(raw)})
        checks["readable:" + name] = error is None
    raw = payloads["events.csv"]
    if raw is not None:
        try:
            lines = raw.decode("utf-8").splitlines()
            import csv
            records = list(csv.DictReader(lines))
            counts = {key: sum(e.get("result") == key for e in records)
                      for key in EXPECTED_COUNT}
            checks["synthetic_event_counts"] = counts == EXPECTED_COUNT
            checks["only_documentation_addresses"] = all(
                e.get("source", "").startswith("192.0.2.") for e in records)
        except (ValueError, UnicodeError, csv.Error):
            checks["synthetic_event_counts"] = False
            checks["only_documentation_addresses"] = False
    else:
        checks["synthetic_event_counts"] = False
        checks["only_documentation_addresses"] = False
    config = (payloads["config/service.txt"] or b"").decode("utf-8", "replace")
    checks["loopback_only"] = "listen=127.0.0.1" in config.splitlines()
    notes = (payloads["notes/investigation.txt"] or b"").decode("utf-8", "replace").upper()
    checks["evidence_and_uncertainty"] = all(
        x in notes for x in ["OBSERVED:", "UNKNOWN:", "NEXT STEP:"])
    if os.name != "nt":
        private = workspace / "permissions/private.txt"
        checks["private_file_mode"] = (
            private.is_file() and not private.is_symlink()
            and (private.stat().st_mode & 0o077) == 0)
    else:
        checks["private_file_mode"] = None
    return {
        "passed": all(value is True for value in checks.values() if value is not None),
        "checks": checks, "artifacts": artifacts,
        "limitations": [
            "Scores fixture state only; it does not prove independent skill or incident attribution.",
            "On Windows, ACL security is not assessed by POSIX mode; review ACLs separately.",
            "All addresses and accounts are fictional. No ports, servers or network tools execute."
        ],
        "questions": [
            "Why do two failed sign-ins not prove account compromise?",
            "How does a SHA-256 digest differ from chain of custody?",
            "Why must you verify the network binding before exposing a service?",
            "What did the verifier NOT test about the real operating system?"
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "check"))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        workspace = normal_workspace(args.workspace)
        result = init(workspace) if args.action == "init" else check(workspace)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))
        print("\nPractice artifacts only; not an independently graded skill exam.")


if __name__ == "__main__":
    main()
