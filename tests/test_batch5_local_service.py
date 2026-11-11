"""Run real loopback requests against the actual Batch 5 training service.

No external network, root/admin permissions, scans, or permanent files.
"""
from __future__ import annotations
import importlib.util
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch5_local_service.py"
spec = importlib.util.spec_from_file_location("batch5_service", SCRIPT)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class Batch5IntegrationTests(unittest.TestCase):
    def test_real_loopback_http_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "academy-owned"
            lab.init(workspace)
            self.assertEqual(lab.load_mode(workspace), "stopped")
            with self.assertRaises(ValueError):
                lab.init(workspace)
            server = ThreadingHTTPServer(("127.0.0.1", 0), lab.handler_factory(workspace))
            self.assertEqual(server.server_address[0], "127.0.0.1")
            thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
            thread.start()
            try:
                port = server.server_address[1]
                initial = lab.inspect(port)
                self.assertFalse(initial["passed"])
                self.assertEqual(initial["observations"]["/health"]["status"], 503)
                lab.set_mode(workspace, "denied")
                denied = lab.inspect(port)
                self.assertFalse(denied["passed"])
                self.assertEqual(denied["observations"]["/health"]["status"], 200)
                self.assertEqual(denied["observations"]["/records"]["status"], 403)
                lab.set_mode(workspace, "bad-data")
                malformed = lab.inspect(port)
                self.assertFalse(malformed["passed"])
                self.assertTrue(malformed["checks"]["records_accessible"])
                self.assertFalse(malformed["checks"]["records_exact"])
                lab.set_mode(workspace, "healthy")
                recovered = lab.inspect(port)
                self.assertTrue(recovered["passed"], recovered)
                self.assertTrue(all(recovered["checks"].values()))
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_safe_workspace_and_connection_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "personal"
            lab.init(folder)
            self.assertEqual(lab.load_mode(folder), "stopped")
            with self.assertRaises(ValueError):
                lab.checked_workspace(str(Path(tmp).anchor))
            with self.assertRaises(ValueError):
                lab.set_mode(folder, "unrecognized")
            # No port listening; a refusal is not an HTTP 503 response.
            server = ThreadingHTTPServer(("127.0.0.1", 0), lab.handler_factory(folder))
            port = server.server_address[1]
            server.server_close()
            report = lab.inspect(port)
            self.assertIsNone(report["observations"]["/health"]["status"])
            self.assertFalse(report["passed"])

if __name__ == "__main__":
    unittest.main()
