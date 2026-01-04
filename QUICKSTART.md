# MicroInX v1.0.x — Quickstart

Minimal, deterministic Blade Insight generator (non-generative).

## Where files live (current repo layout)

Package code:
- `src/microinx/engine.py`
- `src/microinx/run.py`

Package data (manifest-locked):
- `src/microinx/data/templates_v0_3.json`
- `src/microinx/data/microinx_manifest_v1.json`

## Run (repo)

### Callable

```python
from microinx.run import microinx_run

out = microinx_run("later.")
# -> {"template_id": "...", "output_text": "...", "sdt": {"pass": True, "violations": [...]}}
print(out)
