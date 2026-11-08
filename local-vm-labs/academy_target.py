#!/usr/bin/env python3
"""Deliberately vulnerable, synthetic web target. LOCAL LOOPBACK ONLY.

For authorized training inside your own isolated Linux VM. No real user data.
Stop with Ctrl+C. Never forward port 8766 to any network.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
import argparse
import json

HOST = "127.0.0.1"
PORT = 8766
RECORDS = {
    "101": {"owner": "guest", "name": "Public lab visitor", "notes": "Training-only account"},
    "102": {"owner": "owner", "name": "Private lab student", "notes": "TRAIN{OBJECT_AUTHZ_MISSING}"},
}
class Handler(BaseHTTPRequestHandler):
    secure = False
    def do_GET(self):
        url = urlsplit(self.path)
        if self.headers.get("Host") != f"{HOST}:{PORT}":
            return self.reply(403, {"error": "Invalid host"})
        if url.path == "/":
            return self.reply(200, {"message": "Academy intentionally vulnerable local target",
                                     "use": "/account?id=101&as=guest",
                                     "secure_mode": self.secure})
        if url.path != "/account":
            return self.reply(404, {"error": "Not found"})
        query = parse_qs(url.query, keep_blank_values=True)
        if set(query) != {"id", "as"} or any(len(v) != 1 for v in query.values()):
            return self.reply(400, {"error": "Use exactly one id and one as parameter"})
        identity = query["as"][0]
        record = RECORDS.get(query["id"][0])
        if identity not in {"guest", "owner"} or record is None:
            return self.reply(404, {"error": "Training record or identity not found"})
        # This intentionally misses authorization in --vulnerable mode.
        # The 'as' parameter is a lab scenario switch, NOT real authentication.
        if self.secure and record["owner"] != identity:
            return self.reply(403, {"error": "Object access denied (training fix enabled)"})
        self.reply(200, {"account": query["id"][0], "record": record,
                         "warning": "Synthetic data, not real authentication"})
    def reply(self, status, body):
        encoded = json.dumps(body, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Allow-Origin", "null-disabled")
        self.end_headers()
        self.wfile.write(encoded)
    def log_message(self, fmt, *args):
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--secure", action="store_true", help="Enforce owner-level access control")
    args = parser.parse_args()
    Handler.secure = args.secure
    print(f"TRAINING TARGET: http://{HOST}:{PORT}")
    print("Mode:", "PATCHED" if args.secure else "INTENTIONALLY VULNERABLE")
    print("Only local browser/VM access. Stop with Ctrl+C. Do not port-forward.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("Target stopped.")

if __name__ == "__main__":
    main()
