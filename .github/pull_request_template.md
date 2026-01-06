# pull_request_template.md

## Summary

- What changed:
- Why:

## Frozen boundaries (required)

-

## Tests run (required; paste exact commands)

-

```bash
python -m unittest -q discover -s tests -p "test_*.py"
```

-

```bash
python -m unittest -q tests/test_microinx_golden_regression.py
```

-

```bash
MICROINX_DEMO_PORT=0 microinx-demo
```

## Risk surface (1–2 bullets)

- Surface touched: (docs / packaging / adapter / CI / tests)
- Frozen-surface risk: (templates / contract / golden / manifest)