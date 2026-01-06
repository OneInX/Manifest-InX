# README.md

![CI](https://github.com/OneInX-Lab/MicroInX/actions/workflows/microinx_ci.yml/badge.svg) ![Release](https://img.shields.io/github/v/release/OneInX-Lab/MicroInX) ![License](https://img.shields.io/github/license/OneInX-Lab/MicroInX)

## MicroInX

MicroInX is a deterministic micro-insight engine that maps minimal user text into one ultra-compressed BladeInsight using a fixed five-vector model (drift, avoidance, drive, loop, fracture) and a frozen template surface, with SDT enforcing exact template fidelity and hard bans.

## Status

Frozen surface (v1.0/v1.0.2): templates v0.3, SDT gate, OpenAPI contract, golden outputs, and release manifest. Support boundary: see `SUPPORT.md` and `FAQ.md`.

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

PowerShell:

```powershell
$env:MICROINX_DEMO_PORT=0; microinx-demo
```

If you are not using the console script:

```bash
python -m microinx.demo
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
- Template fidelity: SDT requires `output_text` to exactly match the selected canonical template.
- Forbidden-token gate: SDT rejects forbidden tokens/phrases (hard bans).
- Release integrity: `src/microinx/data/microinx_manifest_v1.json` is verified at runtime; hash mismatch triggers refusal.
- Regression lock: `src/microinx/data/golden_cases_v1.json` + `tests/test_microinx_golden_regression.py` enforce exact-match stability.

## Version

- "v1.0.x" / "current release line"