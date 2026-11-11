#!/usr/bin/env python3
"""Academy Batch 5: independent diagnosis and repair of a real localhost service.

Run a training server separately using batch5_local_service.py. This CLI
randomizes a *simulated* service fault, gives observations without the answer,
records the diagnosis before revealing it, then checks the live repaired service.
It does not run shell commands, touch remote hosts, or update Academy progress.
This is a learning challenge, not tamper-resistant or proctored testing.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("academy_batch5_service", ROOT / "batch5_local_service.py")
service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(service)
FAULTS = ("stopped", "denied", "bad-data")
ASSESSMENT_FILE = "independent-assessment.json"


def assessment_path(workspace: Path) -> Path:
    service.config_path(workspace)
    path = workspace / ASSESSMENT_FILE
    if path.is_symlink():
        raise ValueError("Assessment file cannot be a symlink")
    if path.exists() and (not path.is_file() or path.stat().st_size > 4096):
        raise ValueError("Invalid or oversized assessment file")
    return path


def read_assessment(workspace: Path) -> dict:
    path = assessment_path(workspace)
    if not path.is_file():
        raise ValueError("No challenge found; run start first")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or obj.get("fault") not in FAULTS or obj.get("phase") not in ("investigate", "diagnosed"):
        raise ValueError("Assessment data is invalid")
    return obj


def save_assessment(workspace: Path, data: dict, create: bool = False) -> None:
    path = assessment_path(workspace)
    if create and path.exists():
        raise ValueError("Challenge exists; use a new disposable workspace for another attempt")
    with path.open("x" if create else "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2)
        out.write("\n")


def start(workspace: Path, fault: str | None = None) -> dict:
    # Instructor/test can supply fault explicitly; the normal learner CLI chooses one.
    path = assessment_path(workspace)
    if path.exists():
        raise ValueError("Existing attempt cannot be overwritten")
    selected = fault if fault is not None else secrets.choice(FAULTS)
    if selected not in FAULTS:
        raise ValueError("Invalid fault")
    service.set_mode(workspace, selected)
    save_assessment(workspace, {"fault": selected, "phase": "investigate"}, create=True)
    return {"started": True, "message": "Fault prepared. Observe with inspect before diagnosing.",
            "limits": "The exercise is not tamper-resistant. Do not inspect its answer files until submission."}


def inspect(workspace: Path, port: int = service.DEFAULT_PORT) -> dict:
    read_assessment(workspace)
    result = service.inspect(port)
    return {"observations": result["observations"], "checks": result["checks"],
            "prompt": "Determine whether the service is unavailable, denying records, or returning incorrect records. State supporting evidence."}


def diagnose(workspace: Path, answer: str, evidence: str) -> dict:
    data = read_assessment(workspace)
    if data["phase"] != "investigate":
        raise ValueError("Diagnosis already submitted")
    if answer not in FAULTS:
        raise ValueError("Unsupported diagnosis")
    if len(evidence.strip()) < 50:
        raise ValueError("Record at least 50 characters of concrete technical evidence")
    correct = answer == data["fault"]
    data.update({"phase": "diagnosed", "diagnosis": answer,
                 "evidence": evidence.strip()[:1500], "diagnosis_correct": correct})
    save_assessment(workspace, data)
    return {"diagnosis_correct": correct, "diagnosis_points": 3 if correct else 0,
            "reason": {
                "stopped": "Both HTTP endpoints respond 503: the server accepted a request but modeled service readiness is unavailable.",
                "denied": "Health responds 200 but records responds 403: an application access rule denies the record request.",
                "bad-data": "Both respond 200 but records do not match expected contents: availability is not data correctness."
            }[data["fault"]],
            "next": "Repair the locally controlled mode to healthy and run grade. Your initial diagnosis is locked."}


def grade(workspace: Path, port: int = service.DEFAULT_PORT) -> dict:
    data = read_assessment(workspace)
    if data["phase"] != "diagnosed":
        raise ValueError("Submit a diagnosis before grading")
    result = service.inspect(port)
    checks = result["checks"]
    repair_points = sum(1 for passed in checks.values() if passed)
    return {
        "objective_score_out_of_6": (3 if data.get("diagnosis_correct") else 0) + repair_points,
        "diagnosis_points": 3 if data.get("diagnosis_correct") else 0,
        "repair_points": repair_points,
        "checks": checks,
        "fully_repaired": result["passed"],
        "human_review_needed": "Explanation quality, troubleshooting process, authorization and originality are not machine graded.",
        "limitations": "Local service configuration is visible and can be edited. This is not a secure, blinded or proctored exam."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("start", "inspect", "diagnose", "grade"))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--port", type=int, default=service.DEFAULT_PORT)
    parser.add_argument("--answer", choices=FAULTS)
    parser.add_argument("--evidence")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Port must be 1024 to 65535")
    try:
        workspace = service.checked_workspace(args.workspace)
        if args.action == "start":
            result = start(workspace)
        elif args.action == "inspect":
            result = inspect(workspace, args.port)
        elif args.action == "diagnose":
            if not args.answer or not args.evidence:
                parser.error("diagnose requires --answer and --evidence")
            result = diagnose(workspace, args.answer, args.evidence)
        else:
            result = grade(workspace, args.port)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
