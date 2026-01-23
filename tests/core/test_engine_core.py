# tests/core/test_engine_core.py
import unittest

from manifestinx.engine import Engine, FEATURE_DIMS


class TestEngineCore(unittest.TestCase):
    def test_core_is_deterministic(self) -> None:
        e = Engine()
        text = "hello world"

        out1 = e.run_text(text, diagnostics=True)
        out2 = e.run_text(text, diagnostics=True)

        self.assertEqual(out1, out2, "Core output must be bit-for-bit identical for identical input")

    def test_core_output_shape(self) -> None:
        e = Engine()
        out = e.run_text("abc", diagnostics=True)

        self.assertTrue(out["ok"])
        self.assertEqual(out["feature_dim_order"], list(FEATURE_DIMS))
        self.assertEqual(len(out["feature_vector"]), len(FEATURE_DIMS))

        # feature_vector entries should be floats (or ints if your implementation uses ints)
        for v in out["feature_vector"]:
            self.assertIsInstance(v, (float, int))

        self.assertIn(out["dominant_dim"], FEATURE_DIMS)

        # Core MUST NOT ship or imply template catalogs
        self.assertNotIn("template_id", out)
        self.assertNotIn("mapped_vectors", out)
