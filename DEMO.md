# DEMO.md

## Prerequisites

- Python 3.10+ (3.12 supported)
- Editable install (local):

```bash
python -m pip install -e . --no-deps
```

```bash
inxzap-demo
```

```bash
MANIFESTINX_DEMO_PORT=0 inxzap-demo
```

```powershell
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```

If you are not using the console script:

```bash
python -m inxzap.demo
```

Notes:
- This keeps the public “product” entrypoint (`inxzap-demo`) separated from the engine (`manifestinx`).