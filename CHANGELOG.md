# CHANGELOG.md

## v1.0.0

MicroInX v1.0.0 freezes a deterministic micro-insight engine that maps minimal user text into a single BladeInsight using a fixed five-vector model and a frozen 15-template surface, with release integrity enforced via manifest hash verification, template fidelity enforced via exact canonical template matching, and SDT enforcing forbidden-token bans (and other SDT rule checks).

Included packs:
- Release Candidate Pack (v1.0)
- Integration Adapter Pack (v1.0)
- API Contract Pack (v1.0)
- One-Command Demo Pack (v1.0)
- Distribution Pack (v1.0)
- CI Smoke Pack (v1.0)
- Golden Regression Pack (v1.0)
- Repo Index Pack (v1.0)

Behavioral invariants:
- Determinism: identical input text yields identical `{template_id, output_text, sdt}`.
- Manifest integrity refusal: runtime/serve path refuses when any required file hash mismatches the release manifest.
- SDT gate: outputs fail SDT on forbidden tokens, interrogatives, emoji/emoticons, or length violations.
- Template fidelity: selected `template_id` maps to an exact canonical template string (exact-match enforcement).

## v1.0.1

- R01 — Template pack builder hardening (md → json).
- R02 — Documentation clarity: integrity gate vs SDT gate separation.
- R03 — Windows env-var parity command block standardization.
- R04 — Test runner parity: explicit unittest list vs discovery.
- R05 — CI hygiene tightening.

No behavior change; golden outputs unchanged.