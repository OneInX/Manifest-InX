# DOCS_INDEX.md

## Canonical (do not edit)

- **MicroInX Canon — v0.1–v0.2** (`MicroInX Canon v0.1–v0.2.md`) — Continuity record: definition, non-goals, tone rules, SDT mandate.
- **MicroInX Blade Insight Template Library v0.3** (`MicroInX Blade Insight Template Library v0.3.md`) — Frozen template surface (T01–T15) + SDT checklist.
- **MicroInX Implementation v1.0** (`MicroInX Implementation v1.0.md`) — Engine interface, mapping rules, SDT automated checks, test spec.

## Finalized v1.0 packs (do not alter)

- **MicroInX Engine Build v1.0** (`MicroInX Engine Build v1.0.md`) — Deterministic engine skeleton + minimal unit slice.
- **MicroInX Validation Pack v1.0** (`MicroInX Validation Pack v1.0.md`) — Frozen templates JSON + expanded tests + executed evidence.
- **MicroInX Release Candidate Pack v1.0** (`MicroInX Release Candidate Pack v1.0.md`) — Stable entrypoint + release manifest + quickstart.
- **MicroInX Integration Adapter v1.0** (`MicroInX Integration Adapter v1.0.md`) — Local JSON API wrapper gated by release integrity.
- **MicroInX API Contract Pack v1.0** (`MicroInX API Contract Pack v1.0.md`) — Format-stable OpenAPI spec + contract tests.
- **MicroInX One-Command Demo Pack v1.0** (`MicroInX One Command Demo Pack v1.0.md`) — One-command demo wrapper + smoke tests.
- **MicroInX Distribution Pack v1.0** (`MicroInX Distribution Pack v1.0.md`) — Installable package + console entrypoint (`microinx-demo`).
- **MicroInX CI Smoke Pack v1.0** (`MicroInX CI Smoke Pack v1.0.md`) — GitHub Actions workflow for deterministic smoke validation.
- **MicroInX Golden Regression Pack v1.0** (`MicroInX Golden Regression Pack v1.0.md`) — Golden cases + exact-match regression lock.
- **MicroInX Repo Index Pack v1.0** (`MicroInX Repo Index Pack v1.0.md`) — Root README + docs index for navigation.

## Release (how to run / ship)

- `QUICKSTART.md` — Minimal CLI/API usage.
- `CHANGELOG.md` — Version history (behavioral invariants summarized).
- `RELEASE_CHECKLIST.md` — Executable release checklist for GitHub Releases.
- `PACKAGING.md` — Install/package notes for `pip install -e .` + console entrypoint.
- `DEMO.md` — One-command demo usage + expected envelope.
- `ADAPTER_QUICKSTART.md` — Local adapter run/usage notes.
- `API_CONTRACT.md` — Contract notes for the adapter envelope.
- `openapi_microinx_v1.yaml` — OpenAPI contract (format-stable for v1.x).

## Ops / Governance (GitHub)

- `GITHUB_SETTINGS_CHECKLIST.md` — Executable checklist for repo protections (branch rules, required checks, security toggles).
- `.github/CODEOWNERS` — Ownership map for required reviews.
- `.github/pull_request_template.md` — PR intake checklist (frozen-boundary enforcement).
- `.github/ISSUE_TEMPLATE/config.yml` — Issue intake routing + links (non-issue support paths).
- `.github/ISSUE_TEMPLATE/bug_report.md` — Bug report template (forensics-friendly intake).
- `.github/ISSUE_TEMPLATE/feature_request.md` — Feature request template (scope control).
- `.github/dependabot.yml` — Dependency update automation configuration.

## Policies / Community

- `LICENSE` — Repository license.
- `SECURITY.md` — Security reporting policy + contact channel.
- `CONTRIBUTING.md` — Contribution rules (frozen behavior boundaries).
- `CODE_OF_CONDUCT.md` — Community conduct expectations + enforcement/reporting path.
- `SUPPORT.md` — Support routing (what belongs in Issues vs elsewhere).
- `FAQ.md` — FAQ/troubleshooting (common install/demo/port/determinism questions).

## Run Order

- Demo: `microinx-demo`
- Tests (all): `python -m unittest -q discover -s tests -p "test_*.py"`
- Tests (CI parity, explicit):
  - `python -m unittest -q tests/test_microinx_engine.py`
  - `python -m unittest -q tests/test_microinx_api_smoke.py`
  - `python -m unittest -q tests/test_microinx_api_contract.py`
  - `python -m unittest -q tests/test_microinx_demo_smoke.py`
  - `python -m unittest -q tests/test_microinx_golden_regression.py`
- CI: `.github/workflows/microinx_ci.yml`