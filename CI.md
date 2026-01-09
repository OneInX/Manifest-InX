# Manifest-InX CI (v1.0) — Smoke Validation

## What this workflow checks

The GitHub Actions workflow runs on every push and pull request and performs:

1) **Editable install** of the packaged ManifestInX distribution:
- `python -m pip install -e . --no-deps`

2) **Fast deterministic tests** (explicit file list; no discovery):
- python -m unittest -q tests.test_manifestinx_engine
- python -m unittest -q tests.test_manifestinx_api_smoke
- python -m unittest -q tests.test_manifestinx_api_contract
- python -m unittest -q tests.test_manifestinx_demo_smoke
- python -m unittest -q tests.test_manifestinx_golden_regression

3) **Console command smoke** using an **ephemeral port** to avoid collisions:
- `MANIFESTINX_DEMO_PORT=0 inxzap-demo`
- Parses the printed JSON and asserts the stable envelope keys.

No external network calls are required by Manifest-InX itself; the checks exercise only local engine + local HTTP server.

## Run the same checks locally

From repo root:

```bash
python -m pip install -e . --no-deps

python -m unittest -q tests/test_manifestinx_engine.py
python -m unittest -q tests/test_manifestinx_api_smoke.py
python -m unittest -q tests/test_manifestinx_api_contract.py
python -m unittest -q tests/test_manifestinx_demo_smoke.py
python -m unittest -q tests/test_manifestinx_golden_regression.py

MANIFESTINX_DEMO_PORT=0 inxzap-demo
```