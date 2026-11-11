#!/usr/bin/env python3
"""Batch 6: safe offline network evidence and vulnerability triage.

Only reads fixed fictional records bundled in this script. No packets,
network connections, hosts, scans, exploitation, files, or credentials.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter

LOGS = [
    {"time": "09:00", "src": "192.0.2.10", "dst": "198.51.100.20", "service": "https", "result": "allow"},
    {"time": "09:01", "src": "192.0.2.10", "dst": "198.51.100.20", "service": "https", "result": "allow"},
    {"time": "09:02", "src": "192.0.2.11", "dst": "198.51.100.20", "service": "https", "result": "deny"},
    {"time": "09:03", "src": "192.0.2.11", "dst": "198.51.100.20", "service": "https", "result": "deny"},
    {"time": "09:04", "src": "192.0.2.12", "dst": "198.51.100.21", "service": "dns", "result": "timeout"},
]
RISKS = {
    "WEB-01": {
        "asset": "Fictional internal training portal",
        "finding": "HTTP 200 exposes a fictional private route without a role check",
        "likelihood": 3, "impact": 3, "exposed": False,
        "evidence": "Controlled localhost GET /private returns a fictional resource",
        "fix": "Enforce deny-by-default server-side authorization; retest denied and allowed cases",
    },
    "WEB-02": {
        "asset": "Fictional service response",
        "finding": "Missing response hardening headers",
        "likelihood": 2, "impact": 1, "exposed": False,
        "evidence": "Controlled localhost response lacks named browser response headers",
        "fix": "Configure appropriate context-specific headers and test their real effect",
    },
    "NET-01": {
        "asset": "Synthetic name resolver",
        "finding": "Single timeout in a fictional DNS event record",
        "likelihood": 1, "impact": 1, "exposed": False,
        "evidence": "One simulated timeout; no independent service health evidence",
        "fix": "Collect timestamped resolver, interface, route and service telemetry before attributing cause",
    },
}


def summarize() -> dict:
    outcome = Counter(x["result"] for x in LOGS)
    by_source = {}
    for event in LOGS:
        by_source.setdefault(event["src"], Counter())[event["result"]] += 1
    return {
        "records": len(LOGS), "outcomes": dict(outcome),
        "by_source": {key: dict(value) for key, value in sorted(by_source.items())},
        "limitations": [
            "These five fictional records do not establish a threat actor or compromise.",
            "Deny events may be normal policy enforcement, not proof of attack.",
            "One DNS timeout does not prove that the resolver is broken."
        ],
    }


def priorities() -> list[dict]:
    ranked = []
    for finding_id, item in RISKS.items():
        # Teaching score, not CVSS, EPSS, or an independently validated risk formula.
        score = item["likelihood"] * item["impact"]
        ranked.append({"id": finding_id, **item, "teaching_score": score})
    return sorted(ranked, key=lambda x: (-x["teaching_score"], x["id"]))


def check_answers(denied: int, timeout: int, highest: str) -> dict:
    correct = {
        "denied_events": denied == 2,
        "timeout_events": timeout == 1,
        "top_training_priority": highest == "WEB-01",
    }
    return {
        "checks": correct, "score_out_of_3": sum(correct.values()),
        "passed": all(correct.values()),
        "explanations": [
            "Exactly two synthetic records have result=deny.",
            "Exactly one fictional DNS event timed out.",
            "WEB-01 scores 3 × 3 = 9 under this teaching model; this does not replace contextual professional risk assessment."
        ],
    }


def report() -> dict:
    return {
        "scope": "Only Academy fictional events and owned localhost web fixture",
        "summary": summarize(), "ranked_findings": priorities(),
        "required_human_review": [
            "Validate affected assets and authorization boundaries.",
            "Check reliability and completeness of the observed evidence.",
            "Separate symptom from verified exploitability.",
            "Document remediation owner, urgency assumptions, rollback and retest."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("evidence", "prioritize", "report", "check"))
    parser.add_argument("--denied", type=int)
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--highest", choices=sorted(RISKS))
    args = parser.parse_args()
    if args.action == "evidence":
        output = summarize()
    elif args.action == "prioritize":
        output = priorities()
    elif args.action == "report":
        output = report()
    else:
        if None in (args.denied, args.timeout, args.highest):
            parser.error("check requires --denied N --timeout N --highest FINDING")
        output = check_answers(args.denied, args.timeout, args.highest)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
