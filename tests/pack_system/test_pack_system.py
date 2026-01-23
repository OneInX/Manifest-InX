import shutil
import tempfile
import unittest
from pathlib import Path

from manifestinx.pack_system import load_pack, validate_pack


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "test_pack"


class TestPackSystem(unittest.TestCase):
    def test_validate_pack_ok(self):
        report = validate_pack(FIXTURE)
        self.assertTrue(report.ok)
        self.assertEqual(report.issues, ())

    def test_load_pack_readonly_handle(self):
        handle = load_pack(FIXTURE)

        # new entrypoint name + file
        self.assertIsNotNone(handle.entrypoint_path("payload"))

        payload = handle.read_json("payload.json")
        self.assertEqual(payload.get("pack_kind"), "test_fixture")
        self.assertEqual(payload.get("dimensions"), ["d01", "d02", "d03", "d04", "d05"])

    def test_hash_mismatch_rejects(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "pack"
            shutil.copytree(FIXTURE, tmp)

            # mutate pinned file
            p = tmp / "payload.json"
            p.write_text(p.read_text("utf-8") + "\n", encoding="utf-8")

            report = validate_pack(tmp)
            self.assertFalse(report.ok)
            codes = {iss.code for iss in report.issues}
            self.assertIn("SHA256_MISMATCH", codes)


if __name__ == "__main__":
    unittest.main()
