#!/usr/bin/env python3
"""Ethical Hacking Academy Batch 7: integrated hands-on capstone.

Runs only read-only checks against the Academy's TWO existing localhost lab
services and fixed fictional telemetry. Never starts services, changes a
workspace, scans external hosts, saves results, or modifies Academy progress.

The objective score evaluates fixture state, NOT the student's reasoning or
independent professional competence.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("Missing Academy local module: " + filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


service = load_module("academy_capstone_service", "batch5_local_service.py")
web = load_module("academy_capstone_web", "batch6_local_web_assessment.py")
triage = load_module("academy_capstone_triage", "batch6_security_triage.py")

REVIEW_CATEGORIES = (
    "Written scope and evidence provenance",
    "Windows or Linux OS inspection explained accurately",
    "Network observations and competing hypotheses",
    "Web authorization and header implications",
    "Remediation, retest, residual risk and executive summary",
)


def score(*, service_port: int = service.DEFAULT_PORT, web_port: int = web.PORT) -> dict:
    """Perform actual localhost HTTP checks and pure fictional telemetry analysis."""
    service_data = service.inspect(service_port)
    web_data = web.assess(web_port)
    evidence = triage.summarize()
    risks = triage.priorities()

    service_checks = {str(key): bool(value) for key, value in service_data["checks"].items()}
    web_checks = {str(key): bool(value) for key, value in web_data["checks"].items()}

    analysis_checks = {
        "five_synthetic_events": evidence["records"] == 5,
        "denies_are_two": evidence["outcomes"].get("deny") == 2,
        "dns_timeouts_are_one": evidence["outcomes"].get("timeout") == 1,
        "priority_uses_transparent_risk_model": (
            bool(risks) and risks[0]["id"] == "WEB-01"
            and risks[0]["teaching_score"] == 9
        ),
    }
    all_checks = {
        **{"local_service/" + key: value for key, value in service_checks.items()},
        **{"web_security/" + key: value for key, value in web_checks.items()},
        **{"defensive_analysis/" + key: value for key, value in analysis_checks.items()},
    }
    assert len(all_checks) == 14
    return {
        "schema": "ethical-hacking-academy-capstone-v1",
        "objective_score": sum(all_checks.values()),
        "objective_maximum": len(all_checks),
        "fixture_checks_passed": all(all_checks.values()),
        "checks": all_checks,
        "service_observations": service_data["observations"],
        "web_observations": web_data["observations"],
        "fictional_telemetry_summary": evidence,
        "fictional_risk_order": [item["id"] for item in risks],
        "human_review_rubric": {
            "dimensions": list(REVIEW_CATEGORIES),
            "points_each": 4,
            "maximum_points": 20,
            "status": "NOT GRADED — requires independent reviewer",
        },
        "report_questions": [
            "Which response establishes a running HTTP server rather than an unreachable socket?",
            "What evidence supports a server-side access-policy problem versus a stopped service?",
            "How does a web header change differ from fixing authorization?",
            "Why do two denied synthetic network events NOT prove compromise?",
            "Which Windows/Linux commands confirm process, listener and route state?",
            "What uncertainty remains after all green fixture checks?",
        ],
        "limitations": [
            "All network requests target explicit 127.0.0.1 Academy services only.",
            "The fixed synthetic telemetry and risk formula are not genuine attack detection.",
            "A green result demonstrates fixture state, not the learner's own diagnostic skill.",
            "The OS administration and written report require human verification.",
            "Results are printed and not written to Academy progress, exams or cloud storage.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service-port", type=int, default=service.DEFAULT_PORT)
    parser.add_argument("--web-port", type=int, default=web.PORT)
    args = parser.parse_args()
    for value in (args.service_port, args.web_port):
        if not 1024 <= value <= 65535:
            parser.error("ports must be nonprivileged local ports 1024–65535")
    print(json.dumps(score(service_port=args.service_port, web_port=args.web_port), indent=2))


if __name__ == "__main__":
    main()
