# RELEASE_CHECKLIST.md

## MicroInX v1.0.0 release checklist

1) Tests
- Run the fast suite:
  - `python -m unittest -q test_microinx_engine.py test_microinx_api_smoke.py test_microinx_api_contract.py test_microinx_demo_smoke.py test_microinx_golden_regression.py`
- If a pytest runner is configured locally, `pytest -q` must report the same pass/fail outcome as the explicit unittest list.

2) One-command demo (ephemeral port)
- `MICROINX_DEMO_PORT=0 microinx-demo`

3) Golden regression lock
- `python -m unittest -q test_microinx_golden_regression.py`

4) Manifest hash verification
- `python - <<'PY'
import microinx_run
microinx_run.verify_release()
print('manifest_ok')
PY`

5) OpenAPI contract vs adapter envelope
- Confirm these files exist and are the v1.0 contract pair:
  - `openapi_microinx_v1.yaml`
  - `microinx_api.py`
- Run the contract slice:
  - `python -m unittest -q test_microinx_api_contract.py`

6) Docs index current
- Confirm `DOCS_INDEX.md` lists: RC, Adapter, Contract, Demo, Distribution, CI, Golden, Repo Index.

7) Optional tag
- `git tag v1.0.0`