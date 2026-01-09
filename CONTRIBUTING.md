# CONTRIBUTING.md

Manifest-InX accepts issues and pull requests, but all contributions are reviewed at the sole discretion of the maintainers and may be rejected for any reason.

## Frozen behavior boundaries (v1.0 / v1.0.x)

The following are treated as frozen in v1.0.x and will not be accepted via issues or PRs unless an explicit version bump and written rationale are approved:

- Canon tone rules (v0.1–v0.2)
- SDT semantics and forbidden-token gates
- API request/response envelope and required keys
- Template text (T01–T15) and template surface shape
- Golden expected outputs (exact-match cases)

## Preferred contribution types

- Documentation fixes and clarifications
- Test additions that do not change any expected outputs
- Robustness and tooling improvements that do not change deterministic behavior

## Workflow

1. Fork the repo
2. Create a branch
3. Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -q

# Demo smoke (Bash):
MANIFESTINX_DEMO_PORT=0 inxzap-demo

# PowerShell equivalent:
$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo
```

4. Open a pull request with:

- a brief summary
- the test command output (or a short confirmation it passed)
- a note confirming no frozen-boundary changes

## Licensing of contributions

By contributing, you agree your contributions are licensed under the project’s Apache-2.0 license.