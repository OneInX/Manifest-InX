# pull_request_template.md

## Summary

- What changed:
- Why:

## Frozen boundaries (required)

-

## Tests run (required; paste exact commands)

-

```bash
python -m unittest -q tests.test_manifestinx_engine
python -m unittest -q tests.test_manifestinx_api_smoke
python -m unittest -q tests.test_manifestinx_api_contract
python -m unittest -q tests.test_manifestinx_demo_smoke
python -m unittest -q tests.test_manifestinx_golden_regression
```

```bash
MANIFESTINX_DEMO_PORT=0 inxzap-demo
```

```PowerShell
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```


## Risk surface (1–2 bullets)

- Surface touched: (docs / packaging / adapter / CI / tests)
- Frozen-surface risk: (templates / contract / golden / manifest)