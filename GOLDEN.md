# MicroInX Golden Regression (v1)

## What “golden” means

A golden case is an exact-match contract over the stable MicroInX v1.0 surface:

- `template_id` is deterministic for a given `input_text`.
- `output_text` is the exact canonical template text for `template_id`.
- `sdt.pass` and `sdt.violations` are exact-match outputs.

This is a regression lock over engine + templates + SDT behavior.

## Allowed changes

Golden cases do not change in place.

Any intentional behavior change requires:

1) Create a new golden file with a bumped name (example: `golden_cases_v2.json`).
2) Update the test to point to the new file and enforce the new `golden_version`.
3) Record a one-line rationale in this file under “Change Log”.

## How to run locally

From repo root:

```bash
python -m unittest -q tests/test_microinx_golden_regression.py