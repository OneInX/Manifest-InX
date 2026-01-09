# FAQ.md

# Manifest-InX — FAQ + Troubleshooting

## 1) How do I install from a local clone (editable)?

```bash
python -m pip install -e . --no-deps
```

## 2) How do I install from a local clone (non-editable)?

```bash
python -m pip install . --no-deps
```

## 3) How do I run the one-command demo?

```bash
inxzap-demo
```

Module fallback:

```bash
python -m inxzap.demo
```

## 4) The demo says the port is already in use. What do I do?

Use an ephemeral port (recommended):

Bash:

```bash
MANIFESTINX_DEMO_PORT=0 inxzap-demo
```

PowerShell:

```powershell
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```

Or choose a specific free port:

Bash:

```bash
MANIFESTINX_DEMO_PORT=18080 inxzap-demo
```

PowerShell:

```powershell
$env:MANIFESTINX_DEMO_PORT=18080; inxzap-demo
```

## 5) The demo prints “MANIFESTINX_DEMO_PORT must be an int”.

Set it to a numeric value (for example `0` or `18080`). If your shell adds quotes automatically, use a plain integer string.

## 6) What determinism should I expect?

Identical input text yields identical `{template_id, output_text, sdt}`.

## 7) What is SDT (gate) vs integrity (manifest)?

- **SDT** is an output gate: it enforces exact canonical template text and blocks forbidden tokens.
- **Manifest integrity** is a release gate: runtime verifies the hashed release files; a hash mismatch triggers refusal.

## 8) I got a “manifest hash mismatch” or the adapter refuses to start.

Your runtime files do not match the frozen manifest. Reinstall from a clean tag/checkout, or revert local edits to release files.

## 9) How do I run the test suite?

From repo root:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 10) Where do I report security issues?

Follow `SECURITY.md`.

## 11) What should I not file as a GitHub Issue?

Do not file usage coaching, interpretation requests, or “what does this output mean” questions. Use this FAQ and the docs index instead.