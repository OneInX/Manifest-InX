# tests/test_microinx_api_smoke.py
# Smoke slice: API wrapper + determinism + SDT reject + manifest tamper refusal

import json
import os
import tempfile
import threading
import time
import unittest
import urllib.request

from importlib import resources as _ir
try:
    from importlib.metadata import version as _dist_version  # py3.8+
except Exception:  # pragma: no cover
    _dist_version = None

from microinx import api as microinx_api
from microinx import engine as microinx_engine


def _expected_version() -> str:
    # Prefer installed distribution version (works in CI / editable installs)
    if _dist_version is not None:
        return _dist_version("microinx")
    # Fallback: if you expose microinx.__version__
    import microinx
    return getattr(microinx, "__version__", "0.0.0")


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=2) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=2) as r:
        return json.loads(r.read().decode("utf-8"))


class TestMicroInXAdapterSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = microinx_api.make_server("127.0.0.1", 0)
        host, port = cls.httpd.server_address
        cls.base = f"http://{host}:{port}"

        cls.t = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.t.start()
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_S1_health(self):
        r = _get(self.base + "/health")
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["version"], _expected_version())

    def test_S2_insight_deterministic(self):
        payload = {"text": "Need more context and more research; later it depends. I revisit again and still."}
        r1 = _post_json(self.base + "/insight", payload)
        r2 = _post_json(self.base + "/insight", payload)
        self.assertEqual(r1, r2)
        self.assertIn("template_id", r1)
        self.assertIn("output_text", r1)
        self.assertIn("sdt", r1)
        self.assertIn("manifest", r1)
        self.assertTrue(r1["manifest"]["hash_ok"])

    def test_S3_sdt_reject(self):
        # Endpoint-level SDT FAIL is not expected under canonical templates (dev integrity signal).
        # We validate SDT gating directly; /insight always returns the SDT envelope.
        s = microinx_engine.sdt_gate("Maybe you defer by widening input until signal collapses.", "T01")
        self.assertFalse(s["pass"])
        self.assertTrue(any(v.startswith("FORBIDDEN:") for v in s["violations"]))

    def test_S4_manifest_tamper_refuses(self):
        # Stronger proof: tamper -> server refuses to start (make_server raises).
        # Tamper the packaged template resource that verify_release checks.
        from importlib.resources import as_file

        tpl = _ir.files("microinx") / "data" / "templates_v0_3.json"

        with as_file(tpl) as tpl_path:
            orig = tpl_path.read_bytes()
            try:
                tpl_path.write_bytes(orig + b" ")
                with self.assertRaises(Exception):
                    microinx_api.make_server("127.0.0.1", 0)
            finally:
                tpl_path.write_bytes(orig)



if __name__ == "__main__":
    unittest.main(verbosity=2)
