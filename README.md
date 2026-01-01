# README.md

## MicroInX

MicroInX is a deterministic micro-insight engine that maps minimal user text into one ultra-compressed BladeInsight using a fixed five-vector model (drift, avoidance, drive, loop, fracture) and a frozen template surface, with SDT enforcing exact template fidelity and hard bans.

## What it is not

MicroInX is not:
- therapy
- counseling
- coaching
- advice
- psychology
- emotional support

## Quick start

### Install (editable)

```bash
python -m pip install -e . --no-deps
```

### Run one-command demo

```bash
microinx-demo
```

Port override (8080 remains default):

```bash
MICROINX_DEMO_PORT=0 microinx-demo
```

### Run tests

```bash
python -m unittest -q \
  test_microinx_engine.py \
  test_microinx_api_smoke.py \
  test_microinx_api_contract.py \
  test_microinx_demo_smoke.py \
  test_microinx_golden_regression.py
```

## Contract

- OpenAPI: `openapi_microinx_v1.yaml`
- Contract notes: `API_CONTRACT.md`

## Determinism and integrity

- Determinism: identical input text yields identical `{template_id, output_text, sdt}`.
- Release integrity: `microinx_manifest_v1.json` is verified at runtime; hash mismatch triggers refusal.
- Regression lock: `golden_cases_v1.json` + `test_microinx_golden_regression.py` enforce exact-match stability.

## Version

- v1.0.0