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

Source of truth: “MicroInX Canon — v0.1–v0.2”.

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

R01 — patch — Template pack builder hardening (md → json)
- Rationale: formalize the derivation step as a reproducible, non-runtime build artifact.
- Risk: low
- Acceptance check: rebuild templates_v0_3.json from canonical md and reproduce the exact SHA-256 currently enforced.

R02 — patch — Documentation clarity: integrity gate vs SDT gate separation
- Rationale: reduce confusion between manifest refusal, template fidelity, and forbidden-token bans.
- Risk: low
- Acceptance check: docs explicitly label three distinct gates and reference the exact failure modes.

R03 — patch — Windows env-var parity command block standardization
- Rationale: reduce friction running dev-only hooks and tests across PowerShell/CMD/Bash.
- Risk: low
- Acceptance check: docs include working command triplet for MICROINX_DEV_INTEGRITY and demo/CI equivalents.

R04 — patch — Test runner parity: explicit unittest list vs discovery
- Rationale: ensure identical outcomes across runners without relying on implicit discovery differences.
- Risk: low
- Acceptance check: docs show a single canonical “fast suite” command and confirm discovery yields the same set.

R05 — patch — CI hygiene tightening
- Rationale: keep CI deterministic and readable (no duplicated install steps, no stray text in YAML).
- Risk: low
- Acceptance check: GitHub Actions workflow passes on the supported python matrix and prints only expected logs.

### v1.1 (minor) — Small capability additions (preserve envelope + tone rules)

R06 — minor — Korean marker coverage (mapping only; no template changes)
- Rationale: expand supported input language without altering output envelope or tone rules.
- Risk: med
- Acceptance check: add a small Korean PASS slice that selects deterministic template IDs and passes SDT.

R07 — minor — Deterministic variant-selection transparency (doc-level)
- Rationale: explain when the engine selects per-vector variant A vs B without adding new runtime outputs.
- Risk: low
- Acceptance check: docs list the deterministic triggers for variant selection and the global low-score fallback rule.

R08 — minor — Optional dev-only diagnostics (gated; not part of stable API)
- Rationale: improve debugging without expanding public surfaces.
- Risk: med
- Acceptance check: diagnostics are behind an explicit dev flag, never enabled by default, and do not change the stable {template_id, output_text, sdt} tuple.

R09 — minor — Adapter QoL: strict Content-Length parsing and clearer 400 error details (no new error codes)
- Rationale: reduce ambiguous adapter failures while keeping contract-stable shapes and codes.
- Risk: med
- Acceptance check: contract tests pass unchanged; error responses remain within the documented {error, detail?} shape.

R10 — minor — Demo UX: port/host override documentation alignment across demo + adapter + contract
- Rationale: keep one-command demo behavior clear while preserving defaults.
- Risk: low
- Acceptance check: docs show default 8080 behavior, ephemeral-port test mode, and override examples consistently.

R11 — minor — Golden regimen expansion (non-breaking)
- Rationale: strengthen regression lock by covering more composite cases and edge inputs.
- Risk: low
- Acceptance check: append-only is permitted only when new cases do not change any existing expected outputs; otherwise bump the golden version (new file) per policy.