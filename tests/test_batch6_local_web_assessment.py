"""Batch 6 real-loopback web security assessment integration tests.

No public sockets, target scans, credentials, or dependencies outside Python.
"""
import importlib.util
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "local-vm-labs" / "batch6_local_web_assessment.py"
spec = importlib.util.spec_from_file_location("academy_batch6_web", SOURCE)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class Batch6WebTests(unittest.TestCase):
    def test_real_http_findings_hardening_and_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "owned-training"
            lab.init(workspace)
            self.assertEqual(lab.get_mode(workspace), "baseline")
            with self.assertRaises(ValueError):
                lab.init(workspace)
            server = ThreadingHTTPServer(("127.0.0.1", 0), lab.handler(workspace))
            self.assertEqual(server.server_address[0], "127.0.0.1")
            runner = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
            runner.start()
            try:
                port = server.server_address[1]
                weak = lab.assess(port)
                self.assertFalse(weak["passed"])
                self.assertEqual(weak["score_out_of_7"], 2)
                self.assertEqual(weak["observations"]["/private"]["status"], 200)
                self.assertFalse(weak["checks"]["nosniff_header"])
                lab.set_mode(workspace, "hardened")
                healthy = lab.assess(port)
                self.assertTrue(healthy["passed"], healthy)
                self.assertEqual(healthy["score_out_of_7"], 7)
                self.assertEqual(healthy["observations"]["/private"]["status"], 403)
                self.assertEqual(healthy["observations"]["/public"]["headers"].get("X-Content-Type-Options"), "nosniff")
                lab.set_mode(workspace, "baseline")
                self.assertFalse(lab.assess(port)["passed"])
            finally:
                server.shutdown()
                server.server_close()
                runner.join(timeout=2)

    def test_safe_scope_and_invalid_routes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "new"
            lab.init(workspace)
            with self.assertRaises(ValueError):
                lab.workspace_path(Path(tmp).anchor)
            with self.assertRaises(ValueError):
                lab.set_mode(workspace, "attack")
            with self.assertRaises(ValueError):
                lab.fetch_local("/other-target", 18766)
            server = ThreadingHTTPServer(("127.0.0.1", 0), lab.handler(workspace))
            port = server.server_address[1]
            server.server_close()
            offline = lab.assess(port)
            self.assertFalse(offline["passed"])
            self.assertIsNone(offline["observations"]["/public"]["status"])

if __name__ == "__main__":
    unittest.main()
