# CHANGELOG

## v1.0.0

**Manifest-InX** is a deterministic post-AI execution layer that maps minimal user text into a single **InX-Zap** output using a fixed five-vector model and a frozen 15-template surface.

Release integrity is enforced via manifest hash verification; template fidelity is enforced via exact canonical template matching; and SDT enforces forbidden-token bans (and other SDT rule checks).

This initial public release is published under the canonical names and package layout.

### Included packs (build provenance)
- Release Candidate Pack (v1.0)
- Integration Adapter Pack (v1.0)
- API Contract Pack (v1.0)
- One-Command Demo Pack (v1.0)
- Distribution Pack (v1.0)
- CI Smoke Pack (v1.0)
- Golden Regression Pack (v1.0)
- Repo Index Pack (v1.0)

### Added
- Reference wrapper package: `inxzap`
  - Primary CLI entrypoint: `inxzap-demo`

### Changed
- Canonical engine module slug: `manifestinx`
- Canonical distribution/project name: `manifestinx`
- Canonical reference pack wrapper: `inxzap`
- Canonical primary CLI: `inxzap-demo`

### Behavioral invariants (frozen)
- **Determinism:** identical input text yields identical `{template_id, output_text, sdt}`.
- **Manifest integrity refusal:** runtime/serve path refuses when any required file hash mismatches the release manifest.
- **SDT gate:** outputs fail SDT on forbidden tokens, interrogatives, emoji/emoticons, or length violations.
- **Template fidelity:** selected `template_id` maps to an exact canonical template string (exact-match enforcement).

### Frozen behavior surface (non-negotiable)
- Template library content and mapping (frozen 15-template surface)
- SDT semantics (tone + template-fidelity gate)
- API contract envelope (OpenAPI shape)
- Golden expected outputs (exact-match)
- Manifest integrity refusal behavior

### Notes
- No behavior change; golden outputs unchanged.