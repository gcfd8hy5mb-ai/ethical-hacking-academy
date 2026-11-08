#!/usr/bin/env python3
"""Regression tests for two-VM web target; binds only test loopback addresses.

python3 -m unittest -v test_two_vm_lab
"""
from __future__ import annotations
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread
from unittest import TestCase
from unittest.mock import patch
import json

import two_vm_target as t
import two_vm_client as c

class TwoVMLabTests(TestCase):
    def test_target_configuration_is_explicit_and_private(self):
        self.assertEqual(t.TARGET_IP, "10.40.0.80")
        self.assertEqual(t.CLIENT_IP, "10.40.0.20")
        self.assertEqual(c.BASE, "http://10.40.0.80:8766")
        self.assertEqual(len(c.ROUTES), 4)
        with self.assertRaises(RuntimeError):
            t.verify_vm_network("0.0.0.0")
        with self.assertRaises(RuntimeError):
            t.verify_vm_network("192.168.1.50")
        with self.assertRaises(ValueError):
            c.request("https://example.org")

    def test_vulnerable_then_patched_authorization(self):
        with patch.object(t, "CLIENT_IP", "127.0.0.1"), patch.object(t, "TARGET_IP", "127.0.0.1"):
            server = ThreadingHTTPServer(("127.0.0.1", 0), t.Handler)
            port = server.server_address[1]
            with patch.object(t, "PORT", port):
                worker = Thread(target=server.serve_forever, daemon=True)
                worker.start()
                def get(path, host=None):
                    conn = HTTPConnection("127.0.0.1", port, timeout=3)
                    conn.request("GET", path, headers={"Host": host or f"127.0.0.1:{port}"})
                    response = conn.getresponse()
                    value = json.loads(response.read())
                    status = response.status
                    conn.close()
                    return status, value
                try:
                    t.Handler.patched = False
                    status, payload = get("/account?id=102&as=guest")
                    self.assertEqual(status, 200)
                    self.assertIn("TRAIN{TWO_VM_OBJECT_AUTHZ}", payload["record"]["notes"])
                    t.Handler.patched = True
                    self.assertEqual(get("/account?id=102&as=guest")[0], 403)
                    self.assertEqual(get("/account?id=102&as=owner")[0], 200)
                    self.assertEqual(get("/account?id=102&as=owner", host="example.com")[0], 403)
                    self.assertEqual(get("/account?id=102&id=101&as=guest")[0], 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    t.Handler.patched = False

if __name__ == "__main__":
    from unittest import main
    main()
