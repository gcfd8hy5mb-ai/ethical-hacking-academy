#!/usr/bin/env python3
"""Run from local-vm-labs/: python3 -m unittest -v test_academy_console

Tests only temporary training files and a localhost HTTP server.
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

import academy_lab
import academy_console


class LocalBrowserConsoleTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.base = Path(self.temp.name) / "academy-local-lab"
        self.lab_patch = patch.object(academy_lab, "BASE", self.base)
        self.console_patch = patch.object(academy_console, "BASE", self.base)
        self.lab_patch.start()
        self.console_patch.start()

    def tearDown(self):
        self.console_patch.stop()
        self.lab_patch.stop()
        self.temp.cleanup()

    def test_setup_inspect_repair_check_and_export(self):
        self.assertIn("Created", academy_console.action("setup", {}))
        before = academy_console.action("permissions", {})
        self.assertIn("0600", before)
        self.assertIn("timeout", academy_console.action("logs", {}))
        self.assertIn("listen 80 extra;", academy_console.action("config", {}))
        self.assertIn("NOT", academy_console.action("check", {}).replace("false", "NOT"))
        academy_console.action("fix-permissions", {})
        academy_console.action("fix-config", {})
        academy_console.action("save-finding", {"text": "The DNS timeout appears in multiple local log lines. It does not prove malicious activity. Check the resolver and routing under approval."})
        result = academy_console.action("check", {})
        self.assertIn("TRAIN{OFFLINE_LINUX_MISSIONS_COMPLETE}", result)
        academy_console.action("export", {})
        evidence = json.loads((self.base / "evidence.json").read_text())
        self.assertTrue(all(evidence["checks"].values()))

    def test_disallows_unknown_commands_and_bad_input(self):
        with self.assertRaises(ValueError):
            academy_console.action("run-shell", {"command": "whoami"})
        academy_console.action("setup", {})
        with self.assertRaises(ValueError):
            academy_console.action("save-finding", {"text": "x" * 5001})
        with self.assertRaises(ValueError):
            academy_console.action("save-finding", {"text": ["not text"]})

    def test_rejects_symlinked_training_file(self):
        academy_console.action("setup", {})
        target = self.base / "outside.txt"
        target.write_text("Do not modify me.")
        training = self.base / "config" / "web.conf"
        training.unlink()
        training.symlink_to(target)
        with self.assertRaises(ValueError):
            academy_console.action("fix-config", {})
        self.assertEqual(target.read_text(), "Do not modify me.")

    def test_http_requires_correct_origin_host_and_session_token(self):
        old_port, old_origin = academy_console.PORT, academy_console.ORIGIN
        server = ThreadingHTTPServer(("127.0.0.1", 0), academy_console.Handler)
        try:
            academy_console.PORT = server.server_address[1]
            academy_console.ORIGIN = f"http://127.0.0.1:{academy_console.PORT}"
            worker = Thread(target=server.serve_forever, daemon=True)
            worker.start()
            port = academy_console.PORT
            conn = HTTPConnection("127.0.0.1", port, timeout=3)
            conn.request("GET", "/")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertIn("Hands-on filesystem classroom", response.read().decode())
            conn.close()

            body = json.dumps({"action": "setup"})
            common = {"Content-Type": "application/json", "Origin": academy_console.ORIGIN}
            conn = HTTPConnection("127.0.0.1", port, timeout=3)
            conn.request("POST", "/api/action", body, headers=common)
            response = conn.getresponse()
            self.assertEqual(response.status, 403)
            response.read()
            conn.close()

            common["X-Lab-Token"] = academy_console.TOKEN
            conn = HTTPConnection("127.0.0.1", port, timeout=3)
            conn.request("POST", "/api/action", body, headers=common)
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertIn("Created", response.read().decode())
            conn.close()

            common["Origin"] = "https://gcfd8hy5mb-ai.github.io"
            conn = HTTPConnection("127.0.0.1", port, timeout=3)
            conn.request("POST", "/api/action", json.dumps({"action": "environment"}), headers=common)
            response = conn.getresponse()
            self.assertEqual(response.status, 403)
            response.read()
            conn.close()
        finally:
            server.shutdown()
            server.server_close()
            academy_console.PORT, academy_console.ORIGIN = old_port, old_origin


if __name__ == "__main__":
    from unittest import main
    main()
