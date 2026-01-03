# MicroInX — Golden Regression Pack (v1.0) — Sprint 9
# Golden regression lock: exact-match on template_id + output_text + SDT envelope.
# No engine/SDT/template edits; this test is the lock.

import json
import os
import unittest
from pathlib import Path

import microinx
from microinx.run import microinx_run


GOLDEN_PATH = Path(microinx.__file__).resolve().parent / "data" / "golden_cases_v1.json"


class TestMicroInXGoldenRegressionV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(GOLDEN_PATH, "r", encoding="utf-8") as f:
            cls.g = json.load(f)

        if not isinstance(cls.g, dict) or cls.g.get("golden_version") != "v1":
            raise RuntimeError("golden file version mismatch")

        cls.cases = cls.g.get("cases")
        if not isinstance(cls.cases, list) or not cls.cases:
            raise RuntimeError("golden file missing cases")

    def test_golden_cases_v1(self):
        for c in self.cases:
            with self.subTest(case_id=c.get("case_id")):
                self._run_case(c)

    def _run_case(self, c: dict) -> None:
        exp_tid = c["expected_template_id"]
        exp_out = c["expected_output_text"]
        exp_pass = c["expected_sdt_pass"]
        exp_v = c["expected_sdt_violations"]

        if exp_pass:
            r = microinx_run(c["input_text"], lang="auto", source="chat")
            self.assertEqual(r["template_id"], exp_tid)
            self.assertEqual(r["output_text"], exp_out)
            self.assertEqual(r["sdt"]["pass"], exp_pass)
            self.assertEqual(r["sdt"]["violations"], exp_v)
            return

        # SDT rejection case: dev-only integrity hook.
        # Packaging/module paths may change; the public stable entrypoint is microinx_run.microinx_run.
        # Enable this check only when explicitly requested:
        # PowerShell:
#   $env:MICROINX_DEV_INTEGRITY="1"; python -m unittest -q tests/test_microinx_golden_regression.py
# CMD:
#   set MICROINX_DEV_INTEGRITY=1&& python -m unittest -q tests/test_microinx_golden_regression.py
# Bash:
#   MICROINX_DEV_INTEGRITY=1 python -m unittest -q tests/test_microinx_golden_regression.py
        if os.getenv("MICROINX_DEV_INTEGRITY", "") != "1":
            self.skipTest("dev-only integrity hook disabled (set MICROINX_DEV_INTEGRITY=1 to run)")

        import importlib

        try:
            microinx_engine = importlib.import_module("microinx.engine")  # dev-only hook; not part of the stable public surface
        except Exception as e:
            raise RuntimeError("dev-only integrity hook unavailable: cannot import microinx.engine") from e

        s = microinx_engine.sdt_gate(exp_out, exp_tid)
        self.assertEqual(s["pass"], exp_pass)
        self.assertEqual(s["violations"], exp_v)


if __name__ == "__main__":
    unittest.main(verbosity=2)