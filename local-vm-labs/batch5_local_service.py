#!/usr/bin/env python3
"""Batch 5: isolated, real loopback HTTP service and objective repair lab.

Commands (from repo root):
 python3 local-vm-labs/batch5_local_service.py init --workspace ~/academy-batch5
 python3 local-vm-labs/batch5_local_service.py serve --workspace ~/academy-batch5
 python3 local-vm-labs/batch5_local_service.py verify --workspace ~/academy-batch5
 python3 local-vm-labs/batch5_local_service.py fault --workspace ~/academy-batch5 --mode denied

Only 127.0.0.1 is contacted/bound. No remote targets, scanning, shell commands,
elevated permissions or arbitrary file writes. "denied" and "bad-data" are
controlled service simulations, not real OS/network authorization failures.
"""
from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

DEFAULT_PORT = 18765
MODES = ("healthy", "stopped", "denied", "bad-data")
EXPECTED_RECORDS = [{"id": 1, "status": "ok"}, {"id": 2, "status": "ok"}]


def checked_workspace(raw: str) -> Path:
    path = Path(raw).expanduser().absolute()
    if path == Path(path.anchor) or not path.name:
        raise ValueError("Filesystem root is not an acceptable workspace")
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("Symlinked workspace or parent is not allowed")
    return path


def config_path(workspace: Path) -> Path:
    if not workspace.is_dir() or workspace.is_symlink():
        raise ValueError("Run init first using a new personal workspace")
    path = workspace / "service.json"
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 4096:
        raise ValueError("Missing, unsafe or oversized service.json")
    return path


def load_mode(workspace: Path) -> str:
    config = json.loads(config_path(workspace).read_text(encoding="utf-8"))
    if not isinstance(config, dict) or config.get("mode") not in MODES:
        raise ValueError("service.json must contain a valid mode")
    return config["mode"]


def init(workspace: Path) -> None:
    if workspace.exists() or workspace.is_symlink():
        raise ValueError("Refusing to overwrite an existing workspace")
    if not workspace.parent.is_dir():
        raise ValueError("Choose a path beneath an existing directory")
    workspace.mkdir(mode=0o700)
    with (workspace / "service.json").open("x", encoding="utf-8") as stream:
        json.dump({"mode": "stopped"}, stream, indent=2)
        stream.write("\n")


def set_mode(workspace: Path, mode: str) -> None:
    if mode not in MODES:
        raise ValueError("Unknown fault mode")
    path = config_path(workspace)
    # No temp files or editing outside the explicitly designated training path.
    with path.open("w", encoding="utf-8") as stream:
        json.dump({"mode": mode}, stream, indent=2)
        stream.write("\n")


def handler_factory(workspace: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/health", "/records"):
                self.send_error(404, "Training route not found")
                return
            try:
                mode = load_mode(workspace)
            except (ValueError, OSError, json.JSONDecodeError):
                mode = "stopped"
            status = 200
            payload = {}
            if mode == "stopped":
                status, payload = 503, {"state": "unavailable"}
            elif self.path == "/records" and mode == "denied":
                status, payload = 403, {"error": "training policy denies this read"}
            elif self.path == "/health":
                payload = {"state": "ready"}
            elif mode == "bad-data":
                payload = {"records": [{"id": 1, "status": "wrong"}]}
            else:
                payload = {"records": EXPECTED_RECORDS}
            data = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, fmt, *args):
            # No real client identifiers are needed in this loopback exercise.
            pass
    return Handler


def serve(workspace: Path, port: int = DEFAULT_PORT) -> None:
    load_mode(workspace)
    # Literal loopback binding; user cannot supply a host address.
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_factory(workspace))
    print(f"Academy lab: http://127.0.0.1:{port} (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def inspect(port: int = DEFAULT_PORT) -> dict:
    observations = {}
    for path in ("/health", "/records"):
        url = f"http://127.0.0.1:{port}{path}"
        try:
            with urlopen(url, timeout=2) as response:
                status = response.status
                data = response.read(4096)
        except HTTPError as error:
            status = error.code
            data = error.read(4096)
        except (URLError, OSError, TimeoutError) as error:
            observations[path] = {"status": None, "error": type(error).__name__}
            continue
        try:
            payload = json.loads(data)
        except (ValueError, UnicodeError):
            payload = None
        observations[path] = {"status": status, "payload": payload}
    health = observations["/health"]
    records = observations["/records"]
    checks = {
        "service_ready": health.get("status") == 200
                         and health.get("payload") == {"state": "ready"},
        "records_accessible": records.get("status") == 200,
        "records_exact": records.get("payload") == {"records": EXPECTED_RECORDS}
    }
    return {
        "passed": all(checks.values()), "checks": checks, "observations": observations,
        "scope": "127.0.0.1 only; local HTTP exercise, no TLS or production security testing",
        "questions": [
            "Is a connection failure equivalent to an HTTP 503? Why not?",
            "How does HTTP 403 differ from a stopped listener?",
            "Why can HTTP 200 still be incorrect when the payload is wrong?"
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "serve", "verify", "fault"))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--mode", choices=MODES)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("port must be between 1024 and 65535")
    try:
        workspace = checked_workspace(args.workspace)
        if args.action == "init":
            init(workspace)
            print("Created disposable lab in stopped mode. Start serve in another terminal.")
        elif args.action == "serve":
            serve(workspace, args.port)
        elif args.action == "fault":
            if not args.mode:
                parser.error("fault requires --mode")
            set_mode(workspace, args.mode)
            print(f"Updated only lab service.json to mode={args.mode}")
        else:
            load_mode(workspace)
            print(json.dumps(inspect(args.port), indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.error(f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
