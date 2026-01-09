# QUICKSTART

## Demo (one command)

```powershell
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```

## Where files live (current repo layout)

Package code:
- `src/manifestinx/engine.py`
- `src/manifestinx/run.py`

Package data (manifest-locked):
- `src/manifestinx/data/templates_v0_3.json`
- `src/manifestinx/data/manifestinx_manifest_v1.json`

## Run (repo)

### Callable

```python
from manifestinx.run import manifestinx_run

out = manifestinx_run("later.")
# -> {"template_id": "...", "output_text": "...", "sdt": {"pass": True, "violations": [...]}}
print(out)
