# MicroInX v1.0.0 — Quickstart

Minimal, deterministic Blade Insight generator (non-generative).

## Files

Runtime requires (manifest-locked):
- `microinx_run.py`
- `microinx_engine.py`
- `templates_v0_3.json`
- `microinx_manifest_v1.json`

## Install / Run (local)

No packaging assumptions. Run from a directory containing the files above.

### Callable

```python
import microinx_run

out = microinx_run.microinx_run("later.")
# -> {"template_id": "...", "output_text": "...", "sdt": {"pass": True, "violations": [...]}}
print(out)
