#!/usr/bin/env python3
"""Explicitly isolated two-VM practice target (synthetic data only).

Run in an Ubuntu *target* VM whose private NIC is 10.40.0.80/24 on a
dedicated INTERNAL virtual switch, with NO default gateway.
Does not bind wildcard/0.0.0.0. Never bridge this network to a real LAN.
"""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
import ipaddress
import json
import socket

TARGET_IP = "10.40.0.80"
PORT = 8766
TRAINING_NET = ipaddress.ip_network("10.40.0.0/24")
CLIENT_IP = "10.40.0.20"
SAFE_RECORDS = {
    "101": {"owner": "guest", "display": "Public visitor", "notes": "Fictional public account"},
    "102": {"owner": "owner", "display": "Private training account",
            "notes": "TRAIN{TWO_VM_OBJECT_AUTHZ}"},
}

def verify_vm_network(ip=TARGET_IP):
    """Fail closed unless the exact private target IP belongs to this VM."""
    if ip != TARGET_IP or ipaddress.ip_address(ip) not in TRAINING_NET:
        raise RuntimeError("Target may bind only to the documented lab IP")
    # Binding this address fails if no NIC owns it.
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind((TARGET_IP, 0))
    finally:
        probe.close()

class Handler(BaseHTTPRequestHandler):
    patched = False
    def respond(self, code, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        # Bind alone is insufficient: also restrict which peer can use this lab.
        peer = ipaddress.ip_address(self.client_address[0])
        if peer != ipaddress.ip_address(CLIENT_IP):
            return self.respond(403, {"error": "Only the documented attacker VM is allowed"})
        expected_host = f"{TARGET_IP}:{PORT}"
        if self.headers.get("Host") != expected_host:
            return self.respond(403, {"error": "Unexpected Host header"})
        url = urlsplit(self.path)
        if url.path == "/health":
            return self.respond(200, {"lab": "academy-two-vm", "mode": "patched" if self.patched else "vulnerable"})
        if url.path != "/account":
            return self.respond(404, {"error": "No such training route"})
        q = parse_qs(url.query, keep_blank_values=True)
        if set(q) != {"id", "as"} or any(len(v) != 1 for v in q.values()):
            return self.respond(400, {"error": "Expected exactly one id and as parameter"})
        role = q["as"][0]
        record = SAFE_RECORDS.get(q["id"][0])
        if role not in ("guest", "owner") or record is None:
            return self.respond(404, {"error": "Synthetic identity or record missing"})
        # INTENTIONAL TRAINING FLAW. 'as' is a synthetic role selector,
        # not authentication. The patched comparison models a server-side rule.
        if self.patched and record["owner"] != role:
            return self.respond(403, {"error": "Object authorization denied"})
        return self.respond(200, {"id": q["id"][0], "record": record,
                                  "warning": "Fictional scenario, no real login"})
    def log_message(self, fmt, *args):
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patched", action="store_true", help="Enforce owner authorization")
    args = parser.parse_args()
    print(f"Target requires NIC IP {TARGET_IP}, approved peer {CLIENT_IP}, network {TRAINING_NET}")
    verify_vm_network()
    Handler.patched = args.patched
    print(f"Starting {'patched' if args.patched else 'intentionally vulnerable'} synthetic target on {TARGET_IP}:{PORT}")
    print("Do not connect the VM to NAT, bridged adapters, the physical LAN or the internet during practice.")
    print("Stop with Ctrl+C.")
    try:
        ThreadingHTTPServer((TARGET_IP, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("Lab stopped.")

if __name__ == "__main__":
    main()
