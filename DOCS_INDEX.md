# DOCS_INDEX.md

## Canonical (do not edit)

- **MicroInX Canon — v0.1–v0.2** (`MicroInX Canon v0.1–v0.2.md`) — Continuity record: definition, non-goals, tone rules, SDT mandate.
- **MicroInX Blade Insight Template Library v0.3** (`MicroInX Blade Insight Template Library v0.3.md`) — Frozen template surface (T01–T15) and SDT checklist.
- **MicroInX Implementation v1.0** (`MicroInX Implementation v1.0.md`) — Minimal engine interface, mapping rules, SDT automated checks, and test spec.

## Finalized v1.0 packs (do not alter)

- **MicroInX Engine Build v1.0** (`MicroInX Engine Build v1.0.md`) — Deterministic engine skeleton and minimal unit slice.
- **MicroInX Validation Pack v1.0** (`MicroInX Validation Pack v1.0.md`) — Frozen templates JSON + expanded tests + executed evidence.
- **MicroInX Release Candidate Pack v1.0** (`MicroInX Release Candidate Pack v1.0.md`) — Stable entrypoint + release manifest + quickstart.
- **MicroInX Integration Adapter v1.0** (`MicroInX Integration Adapter v1.0.md`) — Local JSON API wrapper that gates on release integrity.
- **MicroInX API Contract Pack v1.0** (`MicroInX API Contract Pack v1.0.md`) — Format-stable OpenAPI spec + contract tests.
- **MicroInX One-Command Demo Pack v1.0** (`MicroInX One Command Demo Pack v1.0.md`) — One-command demo wrapper + smoke tests.
- **MicroInX Distribution Pack v1.0** (`MicroInX Distribution Pack v1.0.md`) — Installable package + console entrypoint (`microinx-demo`).
- **MicroInX CI Smoke Pack v1.0** (`MicroInX CI Smoke Pack v1.0.md`) — GitHub Actions workflow for deterministic smoke validation.
- **MicroInX Golden Regression Pack v1.0** (`MicroInX Golden Regression Pack v1.0.md`) — Golden cases + exact-match regression lock.
- **MicroInX Repo Index Pack v1.0** (`MicroInX Repo Index Pack v1.0.md`) — Root README + docs index for navigation.

## Run Order

- Demo: `microinx-demo`
- Tests: `python -m unittest -q <explicit list>`
- CI: `.github/workflows/microinx_ci.yml`