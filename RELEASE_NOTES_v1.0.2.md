# MicroInX v1.0.2

Patch release. Golden outputs: **unchanged**.

## Changes

- Repository hygiene: add explicit LICENSE for public distribution.
- Public contribution boundary: add CONTRIBUTING.md for minimal, engine-safe contribution guidance.
- Public security contact: add SECURITY.md for vulnerability reporting.
- Cross-platform parity: document PowerShell equivalents for env-var based commands (where applicable).

## Verification

- Golden regression: PASS (`python -m unittest -q tests/test_microinx_golden_regression.py`).
- Contract: PASS (`python -m unittest -q tests/test_microinx_api_contract.py`).
- Demo: PASS (`microinx-demo`).

## Compatibility

- No API contract changes.
- No engine behavior changes; v1.0/v1.0.2 output determinism and SDT enforcement remain frozen.

## Golden policy (explicit)

Golden outputs do not change in place. Any intentional behavior change requires a golden version bump (new golden file/version) rather than editing existing expected outputs.