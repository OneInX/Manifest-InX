import io
import json
import unittest
from contextlib import redirect_stdout

from manifestinx.cli import main


class TestCliJson(unittest.TestCase):
    def test_pack_validate_json_emits_valid_json(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["pack", "validate", "tests/fixtures/test_pack", "--json"])

        self.assertEqual(code, 0)

        payload = json.loads(buf.getvalue())
        self.assertIn("ok", payload)
        self.assertIn("issues", payload)
        self.assertIsInstance(payload["ok"], bool)
        self.assertIsInstance(payload["issues"], list)

    def test_pack_validate_json_reports_failures(self) -> None:
        # Point to a non-pack directory so validation fails deterministically
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["pack", "validate", "tests", "--json"])

        self.assertNotEqual(code, 0)

        payload = json.loads(buf.getvalue())
        self.assertIn("ok", payload)
        self.assertFalse(payload["ok"])
        self.assertIn("issues", payload)
        self.assertIsInstance(payload["issues"], list)
        self.assertGreaterEqual(len(payload["issues"]), 1)
