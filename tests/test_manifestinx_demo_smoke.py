# tests/test_manifestinx_demo_smoke.py
# ManifestInX — One-Command Demo Pack v1.0 (Sprint 6)
# Smoke slice: demo runner envelope + determinism.

import unittest

from manifestinx import demo as manifestinx_demo


class TestmanifestinxDemoSmoke(unittest.TestCase):
    def test_demo_returns_valid_envelope(self):
        r = manifestinx_demo.run_demo(port=0)  # ephemeral port for tests

        self.assertEqual(set(r.keys()), {"template_id", "output_text", "sdt", "manifest"})
        self.assertIsInstance(r["template_id"], str)
        self.assertTrue(len(r["template_id"]) > 0)
        self.assertIsInstance(r["output_text"], str)
        self.assertTrue(len(r["output_text"]) > 0)

        self.assertIsInstance(r["sdt"], dict)
        self.assertEqual(set(r["sdt"].keys()), {"pass", "violations"})
        self.assertIsInstance(r["sdt"]["pass"], bool)
        self.assertIsInstance(r["sdt"]["violations"], list)
        for v in r["sdt"]["violations"]:
            self.assertIsInstance(v, str)

        self.assertIsInstance(r["manifest"], dict)
        self.assertEqual(set(r["manifest"].keys()), {"version", "hash_ok"})
        self.assertIsInstance(r["manifest"]["version"], str)
        self.assertTrue(len(r["manifest"]["version"]) > 0)
        self.assertIsInstance(r["manifest"]["hash_ok"], bool)

    def test_demo_is_deterministic_on_required_tuple(self):
        r1 = manifestinx_demo.run_demo(port=0)
        r2 = manifestinx_demo.run_demo(port=0)

        self.assertEqual(r1["template_id"], r2["template_id"])
        self.assertEqual(r1["output_text"], r2["output_text"])
        self.assertEqual(r1["sdt"], r2["sdt"])


if __name__ == "__main__":
    unittest.main(verbosity=2)