#!/usr/bin/env python3
"""Batch 6: authorized web security assessment on an actual localhost HTTP server.

Standard-library only. No remote targets, credentials, scanning, or exploit
payloads. All requests are forced to 127.0.0.1; server binds loopback only.
Changes are restricted to an explicit disposable workspace.
"""
from __future__ import annotations
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

PORT = 18766
MODES = ("baseline", "hardened")
HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
}
RESOURCE = {"system": "fictional", "service": "academy"}
PUBLIC = {"service": "academy", "scope": "localhost"}


def workspace_path(value: str) -> Path:
    path = Path(value).expanduser().absolute()
    if path == Path(path.anchor) or not path.name:
        raise ValueError("Do not select a filesystem root")
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("Symlinked workspace/parent refused")
    return path


def config_file(path: Path) -> Path:
    if not path.is_dir() or path.is_symlink():
        raise ValueError("Create the disposable workspace first")
    config = path / "web-training.json"
    if config.is_symlink() or not config.is_file() or config.stat().st_size > 1024:
        raise ValueError("Training config must be a small regular file")
    return config


def init(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise ValueError("Existing workspace will not be overwritten")
    if not path.parent.is_dir():
        raise ValueError("Parent directory must exist")
    path.mkdir(mode=0o700)
    with (path / "web-training.json").open("x", encoding="utf-8") as stream:
        json.dump({"mode": "baseline"}, stream)
        stream.write("\n")


def get_mode(path: Path) -> str:
    content = json.loads(config_file(path).read_text(encoding="utf-8"))
    if not isinstance(content, dict) or content.get("mode") not in MODES:
        raise ValueError("Unknown or malformed training mode")
    return content["mode"]


def set_mode(path: Path, mode: str) -> None:
    if mode not in MODES:
        raise ValueError("Invalid training mode")
    config = config_file(path)
    with config.open("w", encoding="utf-8") as stream:
        json.dump({"mode": mode}, stream)
        stream.write("\n")


def handler(path: Path):
    class LocalHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = self.path
            if route not in ("/health", "/public", "/private"):
                return self.reply(404, {"error": "not found"}, False)
            try:
                secure = get_mode(path) == "hardened"
            except (OSError, ValueError, json.JSONDecodeError):
                return self.reply(503, {"error": "fixture unavailable"}, False)
            if route == "/health":
                return self.reply(200, {"state": "ready"}, secure)
            if route == "/public":
                return self.reply(200, PUBLIC, secure)
            if secure:
                return self.reply(403, {"error": "access denied"}, secure)
            return self.reply(200, RESOURCE, secure)

        def reply(self, status: int, body: dict, secure: bool):
            payload = json.dumps(body, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            if secure:
                for name, value in HEADERS.items():
                    self.send_header(name, value)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, fmt, *args):
            pass
    return LocalHandler


def serve(path: Path, port: int = PORT):
    get_mode(path)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler(path))
    print(f"Academy web training on http://127.0.0.1:{port}; Ctrl+C to stop", flush=True)
    try:
        server.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def fetch_local(route: str, port: int) -> dict:
    # URLs are assembled from fixed, known routes and literal loopback host.
    if route not in ("/health", "/public", "/private"):
        raise ValueError("Only known training routes may be requested")
    try:
        with urlopen(f"http://127.0.0.1:{port}{route}", timeout=2) as response:
            status, headers = response.status, dict(response.headers.items())
            body = response.read(2048)
    except HTTPError as error:
        status, headers, body = error.code, dict(error.headers.items()), error.read(2048)
    except (URLError, OSError, TimeoutError) as error:
        return {"status": None, "error": type(error).__name__, "headers": {}, "body": None}
    try:
        content = json.loads(body)
    except (ValueError, UnicodeError):
        content = None
    return {"status": status, "headers": headers, "body": content}


def assess(port: int = PORT) -> dict:
    readings = {route: fetch_local(route, port) for route in ("/health", "/public", "/private")}
    public = readings["/public"]
    private = readings["/private"]
    hdrs = {k.lower(): v for k, v in public["headers"].items()}
    checks = {
        "service_available": readings["/health"]["status"] == 200
                             and readings["/health"]["body"] == {"state": "ready"},
        "public_data_expected": public["status"] == 200 and public["body"] == PUBLIC,
        "private_route_denied": private["status"] == 403
                                and private["body"] == {"error": "access denied"},
        "nosniff_header": hdrs.get("x-content-type-options") == "nosniff",
        "csp_header": hdrs.get("content-security-policy") == HEADERS["Content-Security-Policy"],
        "referrer_header": hdrs.get("referrer-policy") == "no-referrer",
        "cache_header": hdrs.get("cache-control") == "no-store",
    }
    return {
        "checks": checks, "score_out_of_7": sum(checks.values()),
        "passed": all(checks.values()), "observations": readings,
        "limitations": [
            "Only three fictional endpoints and response headers were tested.",
            "The private route is a simulated permission rule with no login or real user data.",
            "Header presence is not sufficient to establish secure application design.",
            "Plain HTTP on loopback is for training only; not a production TLS deployment."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "serve", "assess", "harden", "reset"))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Use a nonprivileged local port from 1024 through 65535")
    try:
        workspace = workspace_path(args.workspace)
        if args.action == "init":
            init(workspace)
            print("Disposable, intentionally weak web fixture created")
        elif args.action == "serve":
            serve(workspace, args.port)
        elif args.action == "assess":
            config_file(workspace)
            print(json.dumps(assess(args.port), indent=2))
        else:
            set_mode(workspace, "hardened" if args.action == "harden" else "baseline")
            print("Training config updated; reassess the running localhost server")
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
