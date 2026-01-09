# Manifest-InX — Distribution Pack (v1.0)

Scope: local installable package wrapper for the finalized Manifest-InX v1.0 stack.

## Install (editable)

From the repo root:

```bash
python -m pip install -e .
```

## Demo

```powershell
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```

## Tests

```bash
python -m unittest discover -s tests -q
```