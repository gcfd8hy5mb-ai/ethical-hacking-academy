"""Batch 7 integrated capstone tests real HTTP against two owned loopback services."""
from __future__ import annotations
import importlib.util
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1] / "local-vm-labs"
spec = importlib.util.spec_from_file_location("batch7_capstone_test", ROOT / "batch7_integrated_capstone.py")
capstone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capstone)


class ServerContext:
    def __init__(self, handler):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            kwargs={"poll_interval": 0.02},
            daemon=True
        )
    def __enter__(self):
        self.thread.start()
        return self
    def __exit__(self, *_):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)


class CapstoneTests(unittest.TestCase):
    def test_real_integration_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            service_dir, web_dir = root / "service", root / "web"
            capstone.service.init(service_dir)
            capstone.web.init(web_dir)
            with ServerContext(capstone.service.handler_factory(service_dir)) as svc, \
                    ServerContext(capstone.web.handler(web_dir)) as site:
                self.assertEqual(svc.server.server_address[0], "127.0.0.1")
                self.assertEqual(site.server.server_address[0], "127.0.0.1")
                baseline = capstone.score(service_port=svc.port, web_port=site.port)
                self.assertEqual(baseline["objective_maximum"], 14)
                self.assertFalse(baseline["fixture_checks_passed"])
                self.assertEqual(baseline["objective_score"], 6)  # 0 service, 2 web, 4 synthetic.
                self.assertEqual(baseline["service_observations"]["/health"]["status"], 503)
                self.assertEqual(baseline["web_observations"]["/private"]["status"], 200)

                capstone.service.set_mode(service_dir, "healthy")
                capstone.web.set_mode(web_dir, "hardened")
                fixed = capstone.score(service_port=svc.port, web_port=site.port)
                self.assertTrue(fixed["fixture_checks_passed"], fixed)
                self.assertEqual(fixed["objective_score"], 14)
                self.assertEqual(fixed["human_review_rubric"]["status"],
                                 "NOT GRADED — requires independent reviewer")
                self.assertEqual(fixed["fictional_risk_order"][0], "WEB-01")

                capstone.web.set_mode(web_dir, "baseline")
                regression = capstone.score(service_port=svc.port, web_port=site.port)
                self.assertFalse(regression["fixture_checks_passed"])
                self.assertEqual(regression["objective_score"], 9)  # 3 service, 2 web, 4 synthetic.
    def test_closed_loopback_services_report_failure(self):
        with ServerContext(capstone.service.handler_factory(Path("unused"))) as s1, \
                ServerContext(capstone.web.handler(Path("unused"))) as s2:
            port1, port2 = s1.port, s2.port
        disconnected = capstone.score(service_port=port1, web_port=port2)
        self.assertEqual(disconnected["objective_score"], 4)
        self.assertIsNone(disconnected["service_observations"]["/health"]["status"])
        self.assertIsNone(disconnected["web_observations"]["/health"]["status"])
        self.assertFalse(disconnected["fixture_checks_passed"])

if __name__ == "__main__":
    unittest.main()
