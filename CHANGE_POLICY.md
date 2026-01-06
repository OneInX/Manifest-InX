## CHANGE_POLICY.md

### Purpose

This document defines MicroInX change control and versioning for the frozen v1.0 / v1.0.2 behavior surface.

### Versioning model (SemVer)

- **Patch (x.y.Z)**: No external behavior change. Determinism, templates, SDT semantics, API envelope, and golden expectations remain identical.
- **Minor (x.Y.z)**: Backward-compatible feature surface expansion (new optional fields/endpoints or new packs) with existing behavior preserved.
- **Major (X.y.z)**: Breaking changes to any frozen surface or to public contract shape/semantics.

### Frozen surfaces

The following surfaces **must not change** without an explicit version bump and a written rationale in the PR:

1) **Template surface v0.3**
- `MicroInX Blade Insight Template Library v0.3.md` (canonical text)
- `src/microinx/data/templates_v0_3.json` (derived mapping; exact strings)

2) **SDT gate semantics** (tone + template fidelity)
- Forbidden-token bans, sentence/word limits, interrogative bans, emoji/emoticon bans
- Exact-template requirement: `output_text` must equal the canonical template string for `template_id`

3) **API contract envelope (OpenAPI)**
- Request/response shapes and required keys for `POST /insight` and `GET /health`
- Error shape `{error, detail?}`

4) **Golden expected outputs (exact-match)**
- `src/microinx/data/golden_cases_v*.json` content
- `tests/test_microinx_golden_regression.py` behavior as an exact-match lock

5) **Manifest integrity refusal behavior**
- `microinx.run.verify_release()` / adapter startup integrity gate
- Hash mismatch results in refusal (no silent fallback)

### Allowed patch changes (examples)

Patch changes are allowed only when they preserve identical outputs for identical inputs across the frozen surface.

- Documentation-only changes (README, docs index, governance docs)
- CI hygiene (workflow reliability) that does not alter required checks’ semantics
- Test additions that do not change existing expectations
- Parser/loader robustness that preserves identical runtime outputs and refusal behavior

### Required version bumps

**Patch bump required** when:
- Packaging/version metadata changes (e.g., `pyproject.toml` version), without changing frozen behavior.
- Internal refactors/robustness changes demonstrably preserve identical outputs.

**Minor bump required** when:
- New additive capability is introduced without breaking existing behavior (e.g., a new optional endpoint, new optional response field, new optional pack) and existing clients continue to work unchanged.

**Major bump required** when any of the following change:
- Any template text (v0.3) or `templates_v0_3.json` strings
- SDT hard-fail rules or exact-template semantics
- OpenAPI contract shape/required keys or endpoint semantics
- Manifest integrity semantics (what is verified, when refusal occurs)

### Golden policy (explicit)

Golden outputs are an exact-match stability lock for `{template_id, output_text, sdt}`.

- **Append-only is allowed** for additional coverage **only if**:
  - All existing golden cases still pass unchanged.
  - No existing expected tuple changes.
  - New cases are added without editing or re-order-dependent semantics.

- **Golden version bump is required** when:
  - Any existing golden case’s expected `template_id`, `output_text`, or `sdt` changes.
  - Any frozen-surface change would alter outputs for any existing golden input.

Golden version bump procedure:
1) Create a new file `src/microinx/data/golden_cases_v<N>.json` with `golden_version: "v<N>"`.
2) Update `tests/test_microinx_golden_regression.py` to point to the new file and enforce the new `golden_version`.
3) Record a one-line rationale in `GOLDEN.md` (Change Log section).

### Required evidence for changes

Every PR that touches code, templates, contract, golden, or manifest must include:

1) **CI parity command set** (run from repo root):

```bash
python -m pip install -e . --no-deps

python -m unittest -q \
  tests/test_microinx_engine.py \
  tests/test_microinx_api_smoke.py \
  tests/test_microinx_api_contract.py \
  tests/test_microinx_demo_smoke.py \
  tests/test_microinx_golden_regression.py

MICROINX_DEMO_PORT=0 microinx-demo
```

2) **Manifest integrity check** (same environment):

```bash
python - <<'PY'
from microinx import run as microinx_run
microinx_run.verify_release()
print('manifest_ok')
PY
```

```powershell
python -c "from microinx import run as microinx_run; microinx_run.verify_release(); print('manifest_ok')"
```

3) **PR includes**:
- A short rationale (what changed and why)
- The required version bump decision (patch/minor/major) and impacted surfaces
- Evidence snippet(s) showing commands executed and passing

### Where to file requests

- Use **GitHub Issues**.
- Bugs: use the **Bug Report** issue template.
- Feature requests / change requests: use the **Feature Request** template.

### Non-negotiables

- No silent behavior drift.
- Frozen surfaces change only with an explicit version bump + rationale + updated golden policy as defined above.