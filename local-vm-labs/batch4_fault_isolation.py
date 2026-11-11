#!/usr/bin/env python3
"""Offline fault-isolation practice: synthetic data only, never executes network commands."""
from __future__ import annotations
import argparse
import json

CASES = {
    "dns": {
        "title": "Name resolution fails while direct routing works",
        "evidence": [
            "ipconfig: IPv4 192.0.2.44/24, gateway 192.0.2.1, DNS 192.0.2.53",
            "ping gateway: reply (synthetic)",
            "nslookup app.training.invalid: DNS request timed out",
            "Application: name lookup failed; no TCP request attempted"
        ],
        "options": {
            "A": "Reset the client DNS resolver or inspect its configured DNS service in the isolated lab",
            "B": "Replace the laptop network card without further evidence",
            "C": "Disable the host firewall and all endpoint protections"
        },
        "correct": "A",
        "reason": "The gateway is reachable but the DNS resolver times out. The next safe step is to inspect configured resolver health, not disable security controls.",
        "limitations": "A simulated timeout does not establish which DNS component failed."
    },
    "route": {
        "title": "Wrong default gateway",
        "evidence": [
            "Client address 198.51.100.10/24; configured gateway 198.51.100.254",
            "Training topology documents gateway 198.51.100.1",
            "Local same-subnet peer reachable; off-subnet requests fail"
        ],
        "options": {
            "A": "Change firewall policy to allow all inbound traffic",
            "B": "Compare documented gateway with client route and correct only the training configuration",
            "C": "Replace DNS certificates"
        },
        "correct": "B",
        "reason": "The off-subnet failure and mismatch with the documented gateway support a routing hypothesis; verify the route after any authorized lab change.",
        "limitations": "The synthetic case does not prove the training gateway is actually operating."
    },
    "service": {
        "title": "Name resolution succeeds; local service is stopped",
        "evidence": [
            "nslookup portal.training.invalid: 203.0.113.20 (synthetic)",
            "Service inventory: portal-service status stopped",
            "Local-only HTTP check: connection refused (synthetic)"
        ],
        "options": {
            "A": "Investigate service state, startup policy and logs before an authorized restart",
            "B": "Treat DNS as broken and set all clients to public resolvers",
            "C": "Scan neighboring network devices for exposed ports"
        },
        "correct": "A",
        "reason": "A resolved name and refused connection can be consistent with no listening service. Confirm bind address, service logs and dependencies.",
        "limitations": "Connection refused can also reflect other endpoint or intermediary behavior."
    },
    "permissions": {
        "title": "Application data denied to a service identity",
        "evidence": [
            "Training directory mode drwx------ owned by student",
            "Fictional service runs as academy-web",
            "Read attempt: permission denied; path exists"
        ],
        "options": {
            "A": "Use chmod -R 777 on the entire system directory",
            "B": "Run all applications as administrator",
            "C": "Inspect path traversal and approved service-account access; propose the narrowest authorized change"
        },
        "correct": "C",
        "reason": "A service identity must be permitted to traverse directories and read only required assets. Least privilege is preferable to broad changes.",
        "limitations": "ACLs, mandatory access controls and filesystem mounts may affect actual access."
    }
}


def review(case_id: str, choice: str) -> dict:
    case = CASES[case_id]
    valid = choice.upper() in case["options"]
    return {
        "case": case_id,
        "valid_selection": valid,
        "correct": valid and choice.upper() == case["correct"],
        "expected": case["correct"],
        "explanation": case["reason"],
        "limitations": case["limitations"],
        "important": "Practice-only interpretation checkpoint; not machine-tested competence."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Show available fictional cases")
    parser.add_argument("--case", choices=sorted(CASES))
    parser.add_argument("--answer", choices=["A", "B", "C", "a", "b", "c"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.list:
        print("\n".join(f"{key}: {value['title']}" for key, value in CASES.items()))
        return
    if not args.case:
        parser.error("Select --case CASE (or --list)")
    case = CASES[args.case]
    if args.answer:
        result = review(args.case, args.answer)
        print(json.dumps(result, indent=2) if args.json else
              ("Correct. " if result["correct"] else "Revisit the evidence. ")
              + result["explanation"] + "\nLimitation: " + result["limitations"])
    else:
        print(case["title"] + "\n\nEvidence:")
        for line in case["evidence"]:
            print(" - " + line)
        print("\nWhich is the safest diagnostic next step?")
        for option, detail in case["options"].items():
            print(f" {option}. {detail}")
        print(f"\nReply using --case {args.case} --answer A|B|C")
        print("This script reads only fictional built-in cases; it does not inspect any network.")


if __name__ == "__main__":
    main()
