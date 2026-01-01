# MicroInX CI (v1.0) — Smoke Validation

## What this workflow checks

The GitHub Actions workflow runs on every push and pull request and performs:

1) **Editable install** of the packaged MicroInX distribution:
- `python -m pip install -e . --no-deps`

2) **Fast deterministic tests** (explicit file list; no discovery):
- `test_microinx_engine.py`
- `test_microinx_api_smoke.py`
- `test_microinx_api_contract.py`
- `test_microinx_demo_smoke.py`

3) **Console command smoke** using an **ephemeral port** to avoid collisions:
- `MICROINX_DEMO_PORT=0 microinx-demo`
- Parses the printed JSON and asserts the stable envelope keys.

No external network calls are required by MicroInX itself; the checks exercise only local engine + local HTTP server.

## Run the same checks locally

From repo root:

```bash
python -m pip install -e . --no-deps

python -m unittest -q \
  test_microinx_engine.py \
  test_microinx_api_smoke.py \
  test_microinx_api_contract.py \
  test_microinx_demo_smoke.py

MICROINX_DEMO_PORT=0 microinx-demo