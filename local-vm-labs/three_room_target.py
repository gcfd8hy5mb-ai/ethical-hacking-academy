#!/usr/bin/env python3
"""Three deliberately vulnerable practice rooms for a TWO-VM INTERNAL network.

Run only in the authorized TARGET VM, 10.40.0.80/24, with no default gateway,
NAT, bridged adapter, host port forwarding, or public exposure. Port 8767.
The query role is a fictional scenario selector, NOT an authentication system.
"""
from __future__ import annotations
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
import ipaddress
import json
import socket

HOST = "10.40.0.80"
CLIENT = "10.40.0.20"
PORT = 8767
NETWORK = ipaddress.ip_network("10.40.0.0/24")
ROOMS = {
    "ownership": {
        "required_role": "owner",
        "guest_role": "guest",
        "key": "id",
        "expected": "102",
        "flag": "TRAIN{ROOM_OBJECT_OWNERSHIP}",
        "description": "Owner-only object 102 must not be readable by a guest.",
    },
    "export": {
        "required_role": "auditor",
        "guest_role": "viewer",
        "key": "report",
        "expected": "q4-internal",
        "flag": "TRAIN{ROOM_REPORT_ACCESS}",
        "description": "Internal audit report must not be exported by viewer role.",
    },
    "debug": {
        "required_role": "administrator",
        "guest_role": "guest",
        "key": "view",
        "expected": "runtime",
        "flag": "TRAIN{ROOM_DEBUG_EXPOSURE}",
        "description": "Internal diagnostics should not be exposed to guests.",
    },
}

def check_binding() -> None:
    """Binding fails closed if the target VM does not actually own its lab IP."""
    if ipaddress.ip_address(HOST) not in NETWORK or HOST != "10.40.0.80":
        raise RuntimeError("Invalid target address")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, 0))
    finally:
        sock.close()

class Handler(BaseHTTPRequestHandler):
    patched = False

    def reply(self, code: int, obj: dict) -> None:
        payload = json.dumps(obj, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if self.client_address[0] != CLIENT:
            return self.reply(403, {"error": "Only the approved investigator address is allowed"})
        if self.headers.get("Host") != f"{HOST}:{PORT}":
            return self.reply(403, {"error": "Unexpected Host header"})
        parsed = urlsplit(self.path)
        if parsed.path == "/health" and not parsed.query:
            return self.reply(200, {"service": "academy-three-rooms", "mode":
                                    "patched" if self.patched else "vulnerable"})
        if not parsed.path.startswith("/room/"):
            return self.reply(404, {"error": "Unknown lab route"})
        name = parsed.path.removeprefix("/room/")
        room = ROOMS.get(name)
        if room is None:
            return self.reply(404, {"error": "Unknown room"})
        q = parse_qs(parsed.query, keep_blank_values=True)
        if set(q) != {"as", room["key"]} or any(len(v) != 1 for v in q.values()):
            return self.reply(400, {"error": "Expected one scenario role and one object selector"})
        role = q["as"][0]
        if role not in (room["guest_role"], room["required_role"]) or q[room["key"]][0] != room["expected"]:
            return self.reply(404, {"error": "Unknown fictional record or scenario role"})
        if self.patched and role != room["required_role"]:
            return self.reply(403, {"error": "Server-side access control rejects this role"})
        return self.reply(200, {
            "room": name, "role": role, "synthetic_data": True,
            "flag": room["flag"], "finding": room["description"],
            "notice": "This role is a training scenario selector, not authentication",
        })

    def log_message(self, fmt, *args):
        pass

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patched", action="store_true", help="Enable access controls in all rooms")
    args = parser.parse_args()
    check_binding()
    Handler.patched = args.patched
    print(f"Training target: {HOST}:{PORT}; approved peer: {CLIENT}; network: {NETWORK}")
    print("Mode:", "PATCHED" if args.patched else "INTENTIONALLY VULNERABLE")
    print("NEVER bridge or forward this service; press Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("Target stopped.")

if __name__ == "__main__":
    main()
