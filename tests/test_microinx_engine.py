# tests/test_microinx_engine.py
# Minimal unit slice: 6 PASS + 4 FAIL (Sprint 1)

import unittest
from pathlib import Path

from microinx.engine import generate_blade_insight, get_templates, sdt_gate
from microinx.template_pack_builder import (
    build_templates_v0_3_json_bytes_from_markdown,
    parse_template_library_markdown,
)


def msignal(raw_text: str):
    return {"raw_text": raw_text, "lang": "auto", "source": "chat", "ts": "2025-01-01T00:00:00Z"}


class TestMicroInXEngineSprint1(unittest.TestCase):
    # ---- PASS (engine path) ----
    def test_P01_drift_T01(self):
        templates = get_templates()
        r = generate_blade_insight(msignal("I will decide later. I need more context before I can lock anything."))
        self.assertEqual(r["template_id"], "T01")
        self.assertEqual(r["output_text"], templates["T01"])
        self.assertTrue(r["sdt"]["pass"])

    def test_P03_avoidance_T03(self):
        templates = get_templates()
        r = generate_blade_insight(msignal("I need 100% certainty before I act. Until then I will wait."))
        self.assertEqual(r["template_id"], "T03")
        self.assertEqual(r["output_text"], templates["T03"])
        self.assertTrue(r["sdt"]["pass"])

    def test_P05_drive_variant_T05(self):
        templates = get_templates()
        r = generate_blade_insight(msignal("Ship today; skip review. Deadline is now."))
        self.assertEqual(r["template_id"], "T05")
        self.assertEqual(r["output_text"], templates["T05"])
        self.assertTrue(r["sdt"]["pass"])

    def test_P09_fracture_T10(self):
        templates = get_templates()
        r = generate_blade_insight(msignal("I call it one label but it means two different things. The meaning changes."))
        self.assertEqual(r["template_id"], "T10")
        self.assertEqual(r["output_text"], templates["T10"])
        self.assertTrue(r["sdt"]["pass"])

    def test_P11_drift_loop_T11(self):
        templates = get_templates()
        r = generate_blade_insight(
            msignal("I need more context and more research; I repeat the same pass again and again. Scope.")
        )
        self.assertEqual(r["template_id"], "T11")
        self.assertEqual(r["mapped_vectors"]["composite"], "drift+loop")
        self.assertEqual(r["output_text"], templates["T11"])
        self.assertTrue(r["sdt"]["pass"])

    def test_P20_short_T02(self):
        templates = get_templates()
        r = generate_blade_insight(msignal("later."))
        self.assertEqual(r["template_id"], "T02")
        self.assertIsNone(r["mapped_vectors"]["secondary"])
        self.assertIsNone(r["mapped_vectors"]["composite"])
        self.assertEqual(r["output_text"], templates["T02"])
        self.assertTrue(r["sdt"]["pass"])

    # ---- FAIL (SDT injection path) ----
    def test_F01_warm_drift_token(self):
        s = sdt_gate("Maybe you defer by widening input until signal collapses.", "T01")
        self.assertFalse(s["pass"])

    def test_F02_advice_token(self):
        s = sdt_gate("You should gate action behind unreachable precision.", "T03")
        self.assertFalse(s["pass"])

    def test_F06_interrogative(self):
        s = sdt_gate("Why do you prioritize the milestone while prerequisites remain unverified?", "T06")
        self.assertFalse(s["pass"])

    def test_F10_emoji(self):
        s = sdt_gate("You defer by letting a weak definition trigger repeated interpretation 🙂", "T11")
        self.assertFalse(s["pass"])


class TestTemplatePackBuilderRobustness(unittest.TestCase):
    def test_R01_builder_canonical_md_matches_frozen_pack_bytes(self):
        repo_root = Path(__file__).resolve().parents[1]
        md_path = repo_root / "src" / "microinx" / "data" / "template_pack_source_v0_3.md"
        pack_path = repo_root / "src" / "microinx" / "data" / "templates_v0_3.json"

        md = md_path.read_text(encoding="utf-8")
        built = build_templates_v0_3_json_bytes_from_markdown(md)
        frozen = pack_path.read_bytes()
        self.assertEqual(built, frozen)

    def test_R01_builder_tolerates_trivial_format_variance(self):
        repo_root = Path(__file__).resolve().parents[1]
        md_path = repo_root / "src" / "microinx" / "data" / "template_pack_source_v0_3.md"
        pack_path = repo_root / "src" / "microinx" / "data" / "templates_v0_3.json"

        canonical_md = md_path.read_text(encoding="utf-8")
        lines = []
        for ln in canonical_md.splitlines():
            s = ln.lstrip()
            if s.startswith("**T") and ("—" in s or "–" in s or " - " in s):
                sep = "—" if "—" in ln else ("–" if "–" in ln else "-")
                ln = "-   " + ln.replace(sep, f"  {sep}   ") + "   "
            lines.append(ln)
        varied_md = "\n".join(lines) + "\n"

        m1 = parse_template_library_markdown(canonical_md)
        m2 = parse_template_library_markdown(varied_md)
        self.assertEqual(m1, m2)

        built = build_templates_v0_3_json_bytes_from_markdown(varied_md)
        frozen = pack_path.read_bytes()
        self.assertEqual(built, frozen)


if __name__ == "__main__":
    unittest.main()
