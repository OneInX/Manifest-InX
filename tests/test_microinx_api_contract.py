# MicroInX — API Contract Pack v1.0 (Sprint 5)
# Contract slice: shape + required keys/types + determinism.

import json
import threading
import time
import unittest
import urllib.request

import microinx_api as microinx_api


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=2) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        return json.loads(r.read().decode("utf-8"))


def _assert_is_str(tc: unittest.TestCase, v, k: str) -> None:
    tc.assertIsInstance(v, str, f"{k} must be string")
    tc.assertTrue(len(v) > 0, f"{k} must be non-empty")


class TestMicroInXAPIContractV1(unittest.TestCase):
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

    def test_contract_health_shape(self):
        r = _get(self.base + "/health")
        self.assertEqual(set(r.keys()), {"status", "version"})
        self.assertEqual(r["status"], "ok")
        _assert_is_str(self, r["version"], "version")

    def test_contract_insight_required_keys_and_types(self):
        payload = {"text": "later."}
        r = _post_json(self.base + "/insight", payload)

        self.assertEqual(set(r.keys()), {"template_id", "output_text", "sdt", "manifest"})

        _assert_is_str(self, r["template_id"], "template_id")
        _assert_is_str(self, r["output_text"], "output_text")

        self.assertIsInstance(r["sdt"], dict)
        self.assertEqual(set(r["sdt"].keys()), {"pass", "violations"})
        self.assertIsInstance(r["sdt"]["pass"], bool)
        self.assertIsInstance(r["sdt"]["violations"], list)
        for v in r["sdt"]["violations"]:
            self.assertIsInstance(v, str)

        self.assertIsInstance(r["manifest"], dict)
        self.assertEqual(set(r["manifest"].keys()), {"version", "hash_ok"})
        _assert_is_str(self, r["manifest"]["version"], "manifest.version")
        self.assertIsInstance(r["manifest"]["hash_ok"], bool)

    def test_contract_determinism_same_input_same_tuple(self):
        payload = {"text": "Need more context and more research; later it depends. I revisit again and still."}
        r1 = _post_json(self.base + "/insight", payload)
        r2 = _post_json(self.base + "/insight", payload)

        self.assertEqual(r1["template_id"], r2["template_id"])
        self.assertEqual(r1["output_text"], r2["output_text"])
        self.assertEqual(r1["sdt"], r2["sdt"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
