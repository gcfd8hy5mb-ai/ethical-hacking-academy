#!/usr/bin/env python3
"""Limited, authorized two-VM lab client; ONLY sends HTTP to 10.40.0.80:8766.

Run inside the separate attacker VM with private NIC 10.40.0.20/24.
No scanning, no shell execution, no arbitrary address/URL parameter.
"""
from __future__ import annotations
import argparse
import json
import urllib.request
import urllib.error

BASE = "http://10.40.0.80:8766"
ROUTES = {
    "health": "/health",
    "guest-public": "/account?id=101&as=guest",
    "guest-private": "/account?id=102&as=guest",
    "owner-private": "/account?id=102&as=owner",
}

def request(action):
    if action not in ROUTES:
        raise ValueError("Unrecognized training action")
    path = ROUTES[action]
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=4) as result:
            return result.status, json.loads(result.read(7000))
    except urllib.error.HTTPError as ex:
        return ex.code, json.loads(ex.read(7000))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=(*ROUTES, "all"))
    args = parser.parse_args()
    print("TRAINING-ONLY target:", BASE)
    for action in (ROUTES if args.action == "all" else [args.action]):
        try:
            status, body = request(action)
            print(f"\n{action}: HTTP {status}\n{json.dumps(body, indent=2)}")
        except urllib.error.URLError as ex:
            print(f"\n{action}: target unreachable ({ex.reason}). Check private NICs, routes, service and firewall.")
            break

if __name__ == "__main__":
    main()
