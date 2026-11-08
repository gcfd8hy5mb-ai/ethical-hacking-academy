#!/usr/bin/env python3
"""Local target regression tests. Run: python3 -m unittest -v test_academy_target"""
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread
from unittest import TestCase
import json

import academy_target

class TrainingTargetTests(TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), academy_target.Handler)
        self.port = self.server.server_address[1]
        self.old_port = academy_target.PORT
        academy_target.PORT = self.port
        academy_target.Handler.secure = False
        self.worker = Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        academy_target.PORT = self.old_port
        academy_target.Handler.secure = False

    def request(self, path, host=None):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=3)
        connection.request("GET", path, headers={"Host": host or f"127.0.0.1:{self.port}"})
        response = connection.getresponse()
        data = json.loads(response.read())
        status = response.status
        connection.close()
        return status, data

    def test_vulnerable_guest_observes_synthetic_private_record(self):
        status, result = self.request("/account?id=102&as=guest")
        self.assertEqual(status, 200)
        self.assertEqual(result["record"]["notes"], "TRAIN{OBJECT_AUTHZ_MISSING}")

    def test_patched_mode_denies_cross_owner(self):
        academy_target.Handler.secure = True
        status, _ = self.request("/account?id=102&as=guest")
        self.assertEqual(status, 403)
        status, _ = self.request("/account?id=102&as=owner")
        self.assertEqual(status, 200)

    def test_rejects_host_rebinding_and_unexpected_inputs(self):
        status, _ = self.request("/account?id=102&as=guest", host="example.com")
        self.assertEqual(status, 403)
        status, _ = self.request("/account?id=102&id=101&as=guest")
        self.assertEqual(status, 400)
        status, _ = self.request("/does-not-exist")
        self.assertEqual(status, 404)

if __name__ == "__main__":
    from unittest import main
    main()
