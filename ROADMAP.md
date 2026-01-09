# ROADMAP.md

## Purpose

Define the next shippable path after v1.0.0 GO: a patch release for robustness with zero semantic change, and a small minor release for capability additions that preserve the v1.x output envelope and tone rules.

## Versioned Change Policy (v1.x)

### Non‑Negotiables remain unchanged (v0.1 restrictions)

- No emojis.
- No empathy, comfort, or reassurance language.
- No advice/coaching verbs (examples: should, try, consider, recommend).
- No psychology framing/terms.
- 1–2 sentences, declarative, ≤40 words.
- Output text equals the canonical template string for the selected template ID (exact match).
- Determinism: identical input text yields identical {template_id, output_text, sdt}.

Source of truth: “Manifest-InX Canon v0.1–v0.2”.

### What counts as a semantic change

Any change that can alter outputs for an existing input under the public surfaces is semantic, including:

- Template text changes (v0.3 surface)
- Mapping/scoring/selection logic changes
- SDT hard checks or forbidden-token lists changes
- Public output keys, error shapes, or contract behavior changes

Semantic changes require: new golden version file (bumped), explicit changelog note, and at least one new regression slice proving determinism and SDT invariants.

### Release types

- **v1.0.1 (patch)**: robustness, packaging/test/CLI/documentation hardening only; no behavior changes for any existing input.
- **v1.1 (minor)**: small capability additions that preserve output envelope and tone rules; allowed to expand supported inputs or add dev tooling if determinism and SDT invariants remain intact.

## Tracks

### v1.0.1 (patch) — Robustness only (zero semantic change)

R01 — patch — Template pack derivation reproducibility test (md → json)
- Rationale: prove `templates_v0_3.json` is derivable from the canonical v0.3 markdown and remains byte-stable.
- Risk: low
- Acceptance check:
  - Add a deterministic test that rebuilds `templates_v0_3.json` from the canonical md and reproduces the exact SHA-256 currently enforced.

R02 — patch — Documentation clarity: integrity gate vs SDT gate separation
- Rationale: reduce confusion between manifest refusal, template fidelity, and forbidden-token bans.
- Risk: low
- Acceptance check:
  - Docs explicitly label the three distinct gates and reference the exact failure modes.

R03 — patch — Python support floor alignment (metadata only)
- Rationale: avoid implying support for Python versions you don’t test.
- Risk: low
- Acceptance check:
  - Align `requires-python` + classifiers with the CI-tested versions (e.g., 3.10/3.12) without changing runtime behavior.

Notes:
- No template text edits.
- No SDT semantic edits.
- No contract envelope edits.
- No golden expected-output edits.

### v1.1 (minor) — Small capability additions (preserve envelope + tone rules)

R04 — minor — Non-English marker coverage (mapping only; no template changes)
- Rationale: expand supported input language without altering output envelope or tone rules.
- Risk: med
- Acceptance check:
  - Existing v1.0 golden outputs remain exact-match.
  - Add a small non-English PASS slice that selects deterministic template IDs and passes SDT.

R05 — minor — Deterministic variant-selection transparency (doc-level)
- Rationale: explain when the engine selects per-vector variant A vs B without adding new runtime outputs.
- Risk: low
- Acceptance check: docs list the deterministic triggers for variant selection and the global low-score fallback rule.

R06 — minor — Optional dev-only diagnostics (gated; not part of stable API)
- Rationale: improve debugging without expanding public surfaces.
- Risk: med
- Acceptance check: diagnostics are behind an explicit dev flag, never enabled by default, and do not change the stable {template_id, output_text, sdt} tuple.

R07 — minor — Adapter QoL: strict Content-Length parsing and clearer 400 error details (no new error codes)
- Rationale: reduce ambiguous adapter failures while keeping contract-stable shapes and codes.
- Risk: med
- Acceptance check: contract tests pass unchanged; error responses remain within the documented {error, detail?} shape.

R08 — minor — Demo UX: port/host override documentation alignment across demo + adapter + contract
- Rationale: keep one-command demo behavior clear while preserving defaults.
- Risk: low
- Acceptance check: docs show default 8080 behavior, ephemeral-port test mode, and override examples consistently.

R09 — minor — Golden regimen expansion (non-breaking)
- Rationale: strengthen regression lock by covering more composite cases and edge inputs.
- Risk: low
- Acceptance check: append-only is permitted only when new cases do not change any existing expected outputs; otherwise bump the golden version (new file) per policy.