# RELEASE_CHECKLIST.md

## MicroInX v1.0.x release checklist (behavior frozen at v1.0.0)

### Gates (keep concepts separate)

- **Integrity gate (manifest/hash)**: `microinx.run.verify_release()` refuses to run if any required file hash mismatches `src/microinx/data/microinx_manifest_v1.json`.
- **SDT gate (tone + template fidelity)**: `microinx.engine.sdt_gate(output_text, template_id)` enforces (a) exact canonical template match, and (b) SDT forbidden-token / tone rules.

---

### 1) Install (editable)

From repo root:

- `python -m pip install -U pip` (optional hardening)
- `python -m pip install -e . --no-deps`

---

### 2) Tests (authoritative commands; aligned with CI)

Run the explicit suite:

- `python -m unittest -q tests/test_microinx_engine.py`
- `python -m unittest -q tests/test_microinx_api_smoke.py`
- `python -m unittest -q tests/test_microinx_api_contract.py`
- `python -m unittest -q tests/test_microinx_demo_smoke.py`
- `python -m unittest -q tests/test_microinx_golden_regression.py`

If a pytest runner is configured locally, `pytest -q` must report the same pass/fail outcome as the explicit unittest list.

---

### 3) One-command demo (ephemeral port)

- Bash: `MICROINX_DEMO_PORT=0 microinx-demo`
- PowerShell: `$env:MICROINX_DEMO_PORT="0"; microinx-demo`

---

### 4) Golden regression lock (must run; no full-suite skip)

- `python -m unittest -q tests/test_microinx_golden_regression.py`

Dev-only SDT rejection sub-check (optional):

- Bash: `MICROINX_DEV_INTEGRITY=1 python -m unittest -q tests/test_microinx_golden_regression.py`
- PowerShell: `$env:MICROINX_DEV_INTEGRITY="1"; python -m unittest -q tests/test_microinx_golden_regression.py`
- CMD: `set MICROINX_DEV_INTEGRITY=1&& python -m unittest -q tests/test_microinx_golden_regression.py`

---

### 5) Manifest hash verification (Integrity gate)

Cross-platform:

- `python -c "from microinx import run as microinx_run; microinx_run.verify_release(); print('manifest_ok')"`

---

### 6) OpenAPI contract vs adapter envelope

Confirm these files exist and are the v1.0 contract pair:

- `openapi_microinx_v1.yaml`
- `src/microinx/api.py` (importable as `microinx.api`)

Run the contract slice:

- `python -m unittest -q tests/test_microinx_api_contract.py`

---

### 7) Docs index current

Confirm `DOCS_INDEX.md` lists: RC, Adapter, Contract, Demo, Distribution, CI, Golden, Repo Index.

---

### 8) Optional tag

- `git tag v1.0.x`
