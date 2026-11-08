#!/usr/bin/env python3
"""Localhost-only tests; run in local-vm-labs/:
python3 -m unittest -v test_three_room_lab
"""
from __future__ import annotations
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from unittest import TestCase
from unittest.mock import patch
import json

import three_room_target as server
import three_room_client as client

class ThreeRoomTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.record = Path(self.temp.name) / "captured.json"
        self.record_patch = patch.object(client, "OUTPUT", self.record)
        self.record_patch.start()
        self.address = patch.object(server, "CLIENT", "127.0.0.1")
        self.host = patch.object(server, "HOST", "127.0.0.1")
        self.address.start()
        self.host.start()
        self.target = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.port = self.target.server_address[1]
        self.port_patch = patch.object(server, "PORT", self.port)
        self.port_patch.start()
        self.base_patch = patch.object(client, "BASE", f"http://127.0.0.1:{self.port}")
        self.base_patch.start()
        self.worker = Thread(target=self.target.serve_forever, daemon=True)
        self.worker.start()
        server.Handler.patched = False

    def tearDown(self):
        self.target.shutdown()
        self.target.server_close()
        server.Handler.patched = False
        self.base_patch.stop()
        self.port_patch.stop()
        self.host.stop()
        self.address.stop()
        self.record_patch.stop()
        self.temp.cleanup()

    def test_three_unprivileged_exposures_then_patched_denials(self):
        self.assertEqual(client.get("/health")["data"]["mode"], "vulnerable")
        for room, case in client.CASES.items():
            output = client.get(case["unauthorized"])
            self.assertEqual(output["status"], 200, room)
            self.assertEqual(output["data"]["flag"], case["flag"])
        client.capture("vulnerable")
        server.Handler.patched = True
        self.assertEqual(client.get("/health")["data"]["mode"], "patched")
        for room, case in client.CASES.items():
            self.assertEqual(client.get(case["unauthorized"])["status"], 403, room)
            self.assertEqual(client.get(case["authorized"])["status"], 200, room)
        client.capture("patched")
        evidence = client.read()["captures"]
        self.assertEqual(len(evidence["vulnerable"]["rooms"]), 3)
        self.assertEqual(len(evidence["patched"]["rooms"]), 3)
        self.assertEqual(client.grade_score()["score"], 100)

    def test_failure_if_target_mode_is_not_changed(self):
        client.capture("vulnerable")
        with self.assertRaises(ValueError):
            client.capture("patched")

    def test_fixed_scope_denies_arbitrary_urls(self):
        with self.assertRaises(ValueError):
            client.get("http://example.org")
        with self.assertRaises(ValueError):
            client.get("/api/arbitrary")
        for room, case in client.CASES.items():
            self.assertIn(case["unauthorized"], [x["unauthorized"] for x in client.CASES.values()])

    def test_patched_mode_preserves_authorized_roles(self):
        server.Handler.patched = True
        for room, case in client.CASES.items():
            self.assertEqual(client.get(case["authorized"])["status"], 200)

    def test_unsupported_query_returns_client_error(self):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=3)
        connection.request("GET", "/room/ownership?id=102&id=101&as=guest",
                           headers={"Host": f"127.0.0.1:{self.port}"})
        response = connection.getresponse()
        self.assertEqual(response.status, 400)
        response.read()
        connection.close()

if __name__ == "__main__":
    from unittest import main
    main()
