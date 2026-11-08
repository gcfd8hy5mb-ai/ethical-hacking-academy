#!/usr/bin/env python3
"""Fixed-scope three-room investigator client for an isolated two-VM lab.

Run in ATTACKER VM at 10.40.0.20. No arbitrary URLs, scans, or shell commands.
Capture vulnerable observations first; then retest after target restarts patched.
Reports are learner-controlled local evidence, not remotely attested proof.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import urllib.error
import urllib.request

BASE = "http://10.40.0.80:8767"
OUTPUT = Path.home() / "academy-three-room-evidence.json"
CASES = {
    "ownership": {
        "unauthorized": "/room/ownership?id=102&as=guest",
        "authorized": "/room/ownership?id=102&as=owner",
        "flag": "TRAIN{ROOM_OBJECT_OWNERSHIP}",
        "explain": "Guest access to someone else's record is a server-side object authorization failure.",
    },
    "export": {
        "unauthorized": "/room/export?report=q4-internal&as=viewer",
        "authorized": "/room/export?report=q4-internal&as=auditor",
        "flag": "TRAIN{ROOM_REPORT_ACCESS}",
        "explain": "A viewer must not export internal audit records without permission checks.",
    },
    "debug": {
        "unauthorized": "/room/debug?view=runtime&as=guest",
        "authorized": "/room/debug?view=runtime&as=administrator",
        "flag": "TRAIN{ROOM_DEBUG_EXPOSURE}",
        "explain": "Internal diagnostic information should not be disclosed to unprivileged roles.",
    },
}
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def get(path: str) -> dict:
    if path != "/health" and path not in {
        case[k] for case in CASES.values() for k in ("unauthorized", "authorized")
    }:
        raise ValueError("Unapproved destination")
    request = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    try:
        with OPENER.open(request, timeout=4) as response:
            code = response.status
            data = json.loads(response.read(6000))
    except urllib.error.HTTPError as exc:
        code = exc.code
        data = json.loads(exc.read(6000))
    if not isinstance(data, dict):
        raise ValueError("Unexpected target response")
    return {"status": code, "data": data}

def read() -> dict:
    if OUTPUT.is_file():
        doc = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if doc.get("schema") == "academy-three-room-evidence-v1":
            return doc
    return {"schema": "academy-three-room-evidence-v1", "captures": {},
            "caveat": "Local learner-controlled observations; no independent attestation."}

def write(doc: dict) -> None:
    OUTPUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

def capture(phase: str) -> None:
    expected = "vulnerable" if phase == "vulnerable" else "patched"
    health = get("/health")
    actual = health["data"].get("mode")
    if health["status"] != 200 or actual != expected:
        raise ValueError(f"Target mode is {actual!r}; expected {expected!r}. Stop and restart target in the correct mode.")
    evidence = {"captured_utc": datetime.now(timezone.utc).isoformat(), "target_mode": actual,
                "health": health, "rooms": {}}
    for room, case in CASES.items():
        evidence["rooms"][room] = {
            "unauthorized": get(case["unauthorized"]),
            "authorized": get(case["authorized"]),
        }
    doc = read()
    doc["captures"][phase] = evidence
    # Repeating vulnerable capture invalidates a previous patched run:
    # a later patched phase must be evidenced after this vulnerable observation.
    if phase == "vulnerable":
        doc["captures"].pop("patched", None)
    write(doc)
    print(f"Captured {phase} mode for {len(CASES)} rooms in {OUTPUT}")
    print("No grading yet: the recorded responses may be incomplete or unexpected.")

def grade() -> None:
    doc = read()
    vulnerable = doc["captures"].get("vulnerable", {}).get("rooms", {})
    patched = doc["captures"].get("patched", {}).get("rooms", {})
    score = 0
    checked = {}
    for room, case in CASES.items():
        before = vulnerable.get(room, {}).get("unauthorized", {})
        after = patched.get(room, {}).get("unauthorized", {})
        authorized = patched.get(room, {}).get("authorized", {})
        leaked = before.get("status") == 200 and before.get("data", {}).get("flag") == case["flag"]
        denied = after.get("status") == 403
        allowed = authorized.get("status") == 200 and authorized.get("data", {}).get("flag") == case["flag"]
        if leaked:
            score += 15
        if denied:
            score += 15
        checked[room] = {"vulnerable_access_observed": leaked,
                         "patched_unauthorized_denied": denied,
                         "patched_authorized_preserved": allowed,
                         "root_cause": case["explain"]}
    if all(x["patched_authorized_preserved"] for x in checked.values()):
        score += 10
    print(json.dumps({"automatic_practice_score": score, "maximum": 100,
                      "components": {"before": 45, "patched_denials": 45,
                                     "all_patched_valid_access": 10},
                      "results": checked,
                      "written_analysis": "Not evaluated; instructor/assessor review required",
                      "independent_real_machine_proof": False}, indent=2))
    if score == 100:
        print("Internal lab observation threshold met, pending instructor review.")
    else:
        print("Review incomplete or failing checks; capture both modes and retest.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "grade", "status"))
    parser.add_argument("--phase", choices=("vulnerable", "patched"))
    args = parser.parse_args()
    if args.action == "capture":
        if not args.phase:
            parser.error("capture requires --phase vulnerable or --phase patched")
        capture(args.phase)
    elif args.action == "grade":
        grade()
    else:
        print(json.dumps(get("/health"), indent=2))

if __name__ == "__main__":
    main()
