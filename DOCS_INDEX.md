# DOCS_INDEX.md

## Canonical (do not edit)

- **Manifest-InX Canon — v0.1–v0.2** (`Manifest-InX Canon v0.1–v0.2.md`) — Continuity record: definition, non-goals, tone rules, SDT mandate.
- **Manifest-InX Blade Insight Template Library v0.3** (`Manifest-InX Blade Insight Template Library v0.3.md`) — Frozen template surface (T01–T15) + SDT checklist.
- **Manifest-InX Implementation v1.0** (`Manifest-InX Implementation v1.0.md`) — Engine interface, mapping rules, SDT automated checks, test spec.

## Finalized v1.0 packs (do not alter)

- **Manifest-InX Engine Build v1.0** (`Manifest-InX Engine Build v1.0.md`) — Deterministic engine skeleton + minimal unit slice.
- **Manifest-InX Validation Pack v1.0** (`Manifest-InX Validation Pack v1.0.md`) — Frozen templates JSON + expanded tests + executed evidence.
- **Manifest-InX Release Candidate Pack v1.0** (`Manifest-InX Release Candidate Pack v1.0.md`) — Stable entrypoint + release manifest + quickstart.
- **Manifest-InX Integration Adapter v1.0** (`Manifest-InX Integration Adapter v1.0.md`) — Local JSON API wrapper gated by release integrity.
- **Manifest-InX API Contract Pack v1.0** (`Manifest-InX API Contract Pack v1.0.md`) — Format-stable OpenAPI spec + contract tests.
- **Manifest-InX One-Command Demo Pack v1.0** (`Manifest-InX One Command Demo Pack v1.0.md`) — One-command demo wrapper + smoke tests.
- **Manifest-InX Distribution Pack v1.0** (`Manifest-InX Distribution Pack v1.0.md`) — Installable package + console entrypoint (`inxzap-demo`).
- **Manifest-InX CI Smoke Pack v1.0** (`Manifest-InX CI Smoke Pack v1.0.md`) — GitHub Actions workflow for deterministic smoke validation.
- **Manifest-InX Golden Regression Pack v1.0** (`Manifest-InX Golden Regression Pack v1.0.md`) — Golden cases + exact-match regression lock.
- **Manifest-InX Repo Index Pack v1.0** (`Manifest-InX Repo Index Pack v1.0.md`) — Root README + docs index for navigation.

## Release (how to run / ship)

- `QUICKSTART.md` — Minimal CLI/API usage.
- `CHANGELOG.md` — Version history (behavioral invariants summarized).
- `RELEASE_CHECKLIST.md` — Executable release checklist for GitHub Releases.
- `PACKAGING.md` — Install/package notes for `pip install -e .` + console entrypoint.
- `DEMO.md` — One-command demo usage + expected envelope.
- `ADAPTER_QUICKSTART.md` — Local adapter run/usage notes.
- `API_CONTRACT.md` — Contract notes for the adapter envelope.
- `openapi_manifestinx_v1.yaml` — OpenAPI contract (format-stable for v1.x).

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

- Demo: `inxzap-demo`
- Tests (all): `python -m unittest discover -s tests -q`
- Tests (CI parity, explicit):
  - `python -m unittest -q tests.test_manifestinx_engine`
  - `python -m unittest -q tests.test_manifestinx_api_smoke`
  - `python -m unittest -q tests.test_manifestinx_api_contract`
  - `python -m unittest -q tests.test_manifestinx_demo_smoke`
  - `python -m unittest -q tests.test_manifestinx_golden_regression`
- CI: `.github/workflows/manifestinx_ci.yml`