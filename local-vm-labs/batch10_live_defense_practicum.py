#!/usr/bin/env python3
"""Batch 10: real loopback HTTP incident practicum, standard-library only.

An intentionally degraded training service is bound ONLY to 127.0.0.1.
It serves fictional data. No real credentials, targets, system privileges or
Academy progress records. Each fresh workspace has one randomly selected fault.
"""
from __future__ import annotations

import argparse
import json
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

FAULTS = {
    "availability": {
        "symptom": "HTTP 503 from both health and report endpoints.",
        "diagnosis": "service_unavailable",
        "repair": "restore_service_configuration",
    },
    "access": {
        "symptom": "Health is ready, but the public report request is rejected.",
        "diagnosis": "overbroad_access_denial",
        "repair": "restore_public_route_policy",
    },
    "integrity": {
        "symptom": "The report returns HTTP 200, but one training record is incorrect.",
        "diagnosis": "bad_application_data",
        "repair": "restore_expected_fixture_data",
    },
    "caching": {
        "symptom": "All routes answer, but the public report lacks a no-store policy.",
        "diagnosis": "missing_cache_control",
        "repair": "enable_no_store_policy",
    },
}
EXPECTED = {"records": [{"id": 1, "state": "ok"}, {"id": 2, "state": "ok"}]}
DIAGNOSES = sorted({v["diagnosis"] for v in FAULTS.values()})
REPAIRS = sorted({v["repair"] for v in FAULTS.values()})


def workspace(raw: str) -> Path:
    p = Path(raw).expanduser().absolute()
    if p == Path(p.anchor) or not p.name:
        raise ValueError("Refusing filesystem root")
    if any(parent.is_symlink() for parent in (p, *p.parents)):
        raise ValueError("Symlink workspace or parent not allowed")
    return p


def case_file(folder: Path) -> Path:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Initialize a fresh training workspace first")
    f = folder / "case.json"
    if f.is_symlink() or not f.is_file() or f.stat().st_size > 8192:
        raise ValueError("Unsafe or missing case.json")
    return f


def read_case(folder: Path) -> dict:
    data = json.loads(case_file(folder).read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or data.get("fault") not in FAULTS
            or type(data.get("fixed")) is not bool
            or type(data.get("attempts")) is not int
            or data["attempts"] < 0
            or data.get("diagnosis") not in DIAGNOSES + [None]):
        raise ValueError("Invalid lab configuration")
    return data


def write_case(folder: Path, data: dict) -> None:
    path = case_file(folder)
    # Only the disposable case.json is modified. No unrelated filesystem paths.
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def initialize(folder: Path) -> None:
    if folder.exists() or folder.is_symlink():
        raise ValueError("Will not overwrite an existing workspace")
    if not folder.parent.is_dir():
        raise ValueError("Choose a child of an existing directory")
    folder.mkdir(mode=0o700)
    data = {"fault": secrets.choice(tuple(FAULTS)), "fixed": False,
            "diagnosis": None, "attempts": 0, "correct_repairs": 0}
    (folder / "case.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Created disposable unknown-fault case. Start 'serve' in another terminal.")


def handler_factory(folder: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/health", "/reports", "/private"):
                self.send_error(404, "Unknown training route")
                return
            try:
                c = read_case(folder)
            except (OSError, ValueError, json.JSONDecodeError):
                self.send_error(503, "Lab state cannot be read")
                return
            fault = None if c["fixed"] else c["fault"]
            status = 200
            if self.path == "/private":
                status, payload = 403, {"error": "training resource forbidden"}
            elif fault == "availability":
                status, payload = 503, {"state": "unavailable"}
            elif self.path == "/health":
                payload = {"state": "ready"}
            elif fault == "access":
                status, payload = 403, {"error": "training public route blocked"}
            elif fault == "integrity":
                payload = {"records": [{"id": 1, "state": "incorrect"}]}
            else:
                payload = EXPECTED
            data = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            if fault != "caching":
                self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_):
            pass
    return Handler


def serve(folder: Path, port: int) -> None:
    read_case(folder)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_factory(folder))
    print(f"Training HTTP server on http://127.0.0.1:{server.server_port}; Ctrl+C to stop", flush=True)
    try:
        server.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def request(path: str, port: int) -> dict:
    # Literal 127.0.0.1 prevents external targets; no arbitrary URLs accepted.
    try:
        with urlopen(f"http://127.0.0.1:{port}{path}", timeout=2) as response:
            status, headers, raw = response.status, dict(response.headers), response.read(4096)
    except HTTPError as error:
        status, headers, raw = error.code, dict(error.headers), error.read(4096)
    except (URLError, OSError, TimeoutError) as error:
        return {"status": None, "error": type(error).__name__}
    try:
        payload = json.loads(raw)
    except (ValueError, UnicodeError):
        payload = None
    return {"status": status, "payload": payload,
            "cache_control": headers.get("Cache-Control", "")}


def inspect(port: int) -> dict:
    return {route: request(route, port) for route in ("/health", "/reports", "/private")}


def submit(folder: Path, diagnosis: str) -> None:
    if diagnosis not in DIAGNOSES:
        raise ValueError("Unsupported diagnosis")
    c = read_case(folder)
    if c["diagnosis"] is not None:
        raise ValueError("Diagnosis locked; cannot change after initial submission")
    c["diagnosis"] = diagnosis
    write_case(folder, c)
    print("First diagnosis recorded; now apply a scoped remediation.")


def repair(folder: Path, action: str) -> None:
    if action not in REPAIRS:
        raise ValueError("Only allowlisted training repairs are supported")
    c = read_case(folder)
    c["attempts"] += 1
    correct = action == FAULTS[c["fault"]]["repair"]
    if correct:
        c["fixed"] = True
        c["correct_repairs"] += 1
    write_case(folder, c)
    print("Training configuration updated." if correct else
          "The selected repair did not resolve the lab fault; inspect again.")


def grade(folder: Path, port: int) -> dict:
    c = read_case(folder)
    observations = inspect(port)
    diagnostic = c["diagnosis"] == FAULTS[c["fault"]]["diagnosis"]
    health = observations["/health"]
    reports = observations["/reports"]
    private = observations["/private"]
    checks = {
        "first_diagnosis_correct": diagnostic,
        "repair_applied": c["fixed"],
        "bounded_repair_attempt": c["fixed"] and c["attempts"] == 1,
        "health_returns_ready": health.get("status") == 200 and
                                health.get("payload") == {"state": "ready"},
        "public_report_exact": reports.get("status") == 200 and
                               reports.get("payload") == EXPECTED,
        "cache_control_safe": reports.get("cache_control", "").lower() == "no-store",
        "unauthorized_private_denied": private.get("status") == 403 and
                                       private.get("payload") == {"error": "training resource forbidden"},
    }
    weights = {"first_diagnosis_correct": 2, "repair_applied": 1,
               "bounded_repair_attempt": 1, "health_returns_ready": 2,
               "public_report_exact": 2, "cache_control_safe": 1,
               "unauthorized_private_denied": 1}
    points = sum(weights[k] for k, passed in checks.items() if passed)
    return {"score": points, "maximum": 10, "pass": points >= 8 and
            checks["unauthorized_private_denied"] and checks["public_report_exact"],
            "checks": checks, "observations": observations,
            "scope": "127.0.0.1 only; real HTTP of synthetic data",
            "limits": "The published source exposes fixture answers; writing quality and real-world skill are not auto-graded."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("init", "serve", "inspect", "submit", "repair", "grade", "options"))
    p.add_argument("--workspace", default="academy-batch10")
    p.add_argument("--port", type=int, default=18767)
    p.add_argument("--diagnosis", choices=DIAGNOSES)
    p.add_argument("--action", choices=REPAIRS)
    args = p.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        p.error("Use port 1024–65535")
    try:
        folder = workspace(args.workspace)
        if args.command == "init":
            initialize(folder)
        elif args.command == "serve":
            serve(folder, args.port)
        elif args.command == "inspect":
            print(json.dumps(inspect(args.port), indent=2))
        elif args.command == "options":
            print("Diagnoses:", ", ".join(DIAGNOSES))
            print("Repairs:", ", ".join(REPAIRS))
        elif args.command == "submit":
            if args.diagnosis is None:
                p.error("--diagnosis is required")
            submit(folder, args.diagnosis)
        elif args.command == "repair":
            if args.action is None:
                p.error("--action is required")
            repair(folder, args.action)
        else:
            print(json.dumps(grade(folder, args.port), indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as err:
        print("Batch 10 lab error: " + str(err), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
