# test_microinx_engine.py
# Minimal unit slice: 6 PASS + 4 FAIL (Sprint 1)


import unittest
from microinx_engine import generate_blade_insight, sdt_gate, TEMPLATES




def msignal(raw_text: str):
        return {"raw_text": raw_text, "lang": "auto", "source": "chat", "ts": "2025-01-01T00:00:00Z"}




class TestMicroInXEngineSprint1(unittest.TestCase):
# ---- PASS (engine path) ----
    def test_P01_drift_T01(self):
        r = generate_blade_insight(msignal("I will decide later. I need more context before I can lock anything."))
        self.assertEqual(r["template_id"], "T01")
        self.assertEqual(r["output_text"], TEMPLATES["T01"])
        self.assertTrue(r["sdt"]["pass"])


    def test_P03_avoidance_T03(self):
        r = generate_blade_insight(msignal("I need 100% certainty before I act. Until then I will wait."))
        self.assertEqual(r["template_id"], "T03")
        self.assertTrue(r["sdt"]["pass"])


    def test_P07_loop_T08(self):
        r = generate_blade_insight(msignal("I restart the same plan again and again. There is no stop condition."))
        self.assertEqual(r["template_id"], "T08")
        self.assertTrue(r["sdt"]["pass"])


    def test_P09_fracture_T10(self):
        r = generate_blade_insight(msignal("I call it one label but it means two different things depending on the day."))
        self.assertEqual(r["template_id"], "T10")
        self.assertTrue(r["sdt"]["pass"])


    def test_P11_drift_loop_T11(self):
        r = generate_blade_insight(msignal("I need more context and more research; I repeat the same pass again and again. Scope."))
        self.assertEqual(r["template_id"], "T11")
        self.assertEqual(r["mapped_vectors"]["composite"], "drift+loop")
        self.assertTrue(r["sdt"]["pass"])


    def test_P20_short_T02(self):
        r = generate_blade_insight(msignal("later."))
        self.assertEqual(r["template_id"], "T02")
        self.assertIsNone(r["mapped_vectors"]["secondary"])
        self.assertIsNone(r["mapped_vectors"]["composite"])
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


if __name__ == "__main__":
    unittest.main()