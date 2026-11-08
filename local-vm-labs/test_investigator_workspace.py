#!/usr/bin/env python3
"""Local regression tests for multi-stage workspace.
Run from local-vm-labs: python3 -m unittest -v test_investigator_workspace
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

import investigator_workspace as app


class WorkspaceTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.report = Path(self.temp.name) / "report.json"
        self.report_patch = patch.object(app, "REPORT", self.report)
        self.report_patch.start()
        self.saved_capture = {"captures": {}}
        self.evidence_patch = patch.object(app.lab, "read", side_effect=lambda: self.saved_capture)
        self.evidence_patch.start()
        self.grade_patch = patch.object(app.lab, "grade_score", side_effect=lambda: {
            "score": 100 if "patched" in self.saved_capture["captures"] else 0,
            "maximum": 100, "results": {},
        })
        self.grade_patch.start()

        def simulate_capture(phase):
            self.saved_capture["captures"][phase] = {"rooms": {}}

        self.capture_patch = patch.object(app.lab, "capture", side_effect=simulate_capture)
        self.capture_patch.start()

    def tearDown(self):
        self.capture_patch.stop()
        self.grade_patch.stop()
        self.evidence_patch.stop()
        self.report_patch.stop()
        self.temp.cleanup()

    def test_stages_in_order_and_locked_after_submission(self):
        with self.assertRaises(ValueError):
            app.api_action({"action": "capture-vulnerable"})
        app.api_action({"action": "scope", "confirmed": True})
        with self.assertRaises(ValueError):
            app.api_action({"action": "capture-patched"})
        app.api_action({"action": "capture-vulnerable"})
        with self.assertRaises(ValueError):
            app.api_action({"action": "capture-patched"})
        for room in app.ROOMS:
            app.api_action({"action": "analysis", "room": room,
                            "text": ("Evidence indicates unauthorized access and missing server-side "
                                     "role checks, while this HTTP response alone does not establish "
                                     "identity or intent. The investigator must record the request, "
                                     "expected permission, observed response, relevant synthetic data, "
                                     "scoped remediation, negative test, positive authorized test, "
                                     "and a remaining validation question. " * 2)})
        app.api_action({"action": "capture-patched"})
        app.api_action({"action": "remediation", "text":
                        ("Apply authorization rules server-side, preserve approved roles, "
                         "verify denied access and permitted access, document expected HTTP "
                         "responses, retest every scenario, and review identity assumptions. " * 4)})
        result = app.api_action({"action": "submit"})
        self.assertTrue(result["candidate_ready"])
        self.assertTrue(result["report"]["submitted"])
        with self.assertRaises(ValueError):
            app.api_action({"action": "capture-vulnerable"})

    def test_rejects_invalid_room_or_oversized_text(self):
        app.api_action({"action": "scope", "confirmed": True})
        app.api_action({"action": "capture-vulnerable"})
        with self.assertRaises(ValueError):
            app.api_action({"action": "analysis", "room": "arbitrary", "text": "test"})
        with self.assertRaises(ValueError):
            app.api_action({"action": "analysis", "room": "ownership", "text": "x" * 7501})

    def test_rejects_untrusted_browser_posts(self):
        original_port, original_origin = app.PORT, app.ORIGIN
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        try:
            app.PORT = server.server_address[1]
            app.ORIGIN = f"http://127.0.0.1:{app.PORT}"
            Thread(target=server.serve_forever, daemon=True).start()
            port = app.PORT

            def call(headers):
                con = HTTPConnection("127.0.0.1", port, timeout=3)
                con.request("POST", "/api/workspace", json.dumps({"action": "status"}),
                            headers=headers)
                response = con.getresponse()
                code = response.status
                response.read()
                con.close()
                return code

            base = {"Content-Type": "application/json", "Origin": app.ORIGIN,
                    "X-Workspace-Token": app.TOKEN}
            self.assertEqual(call(base), 200)
            self.assertEqual(call({k: v for k, v in base.items() if k != "X-Workspace-Token"}), 403)
            self.assertEqual(call({**base, "Origin": "https://example.org"}), 403)
            self.assertEqual(call({**base, "Host": "example.org"}), 403)
        finally:
            server.shutdown()
            server.server_close()
            app.PORT, app.ORIGIN = original_port, original_origin


if __name__ == "__main__":
    from unittest import main
    main()
