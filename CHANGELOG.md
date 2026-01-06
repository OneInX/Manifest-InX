# CHANGELOG.md

## v1.0.2

### Fixed
- Template-pack builder newline normalization (LF)
  - Normalize generated template-pack source output to LF newlines to avoid cross-platform diffs (Windows CRLF vs *nix LF).
  - Reduces “false change” noise in template-pack artifacts and keeps frozen-template surfaces byte-stable across environments.

### Changed
- Version hygiene
  - Align version metadata across packaging/release surfaces (package version, tag/release notes alignment, and any referenced manifest/version fields used for release integrity).
  - No mapping/engine behavior changes; versioning only.

- README.md (landing-page tightening)
  - Added a minimal badge strip (CI workflow, latest release, license) at the top for repo status visibility.
  - Added a short “Status” block (≤6 lines) stating frozen surfaces (templates/SDT/API/golden/manifest) and routing to SUPPORT.md + FAQ.md.
  - Added PowerShell parity for demo port override (`$env:MICROINX_DEMO_PORT=0; microinx-demo`).

### Added (release communications)
- RELEASE_NOTES_v1.0.2.md
  - Short, structural release notes for v1.0.2 (docs/governance focus; frozen behavior unchanged).
- GITHUB_RELEASE_CHECKLIST_v1.0.2.md
  - Executable publish checklist for GitHub Releases to reduce missed steps and enforce frozen boundaries.

### Added (repo hygiene + support routing)
- LICENSE
  - Clarifies distribution terms for the public repo.
- CONTRIBUTING.md
  - Defines contribution boundaries consistent with frozen v1.0/v1.0.2 surfaces (templates/SDT/API/golden/manifest).
- SECURITY.md
  - Defines a private reporting path and disclosure expectations (route security issues away from public Issues).
- SUPPORT.md
  - Defines support boundary, contact/routing expectations, and what maintainers will/won’t handle.
- FAQ.md
  - Short troubleshooting + common questions to reduce issue load and route usage questions away from GitHub Issues.
- CODE OF CONDUCT.md
  - Minimal community behavior expectations + reporting path.
- CITATION.cff
  - Citation metadata for academic/reference use (standard CFF format).
- CHANGE_POLICY.md
  - Change-control policy defining what is frozen vs what can change, and how changes are proposed/accepted.

### Added (governance + GitHub ops scaffolding)
- GITHUB_SETTINGS_CHECKLIST.md
  - Executable repo-settings checklist (branch protection, required checks, security toggles) to protect the frozen v1.0.2 surface.
- DOCS_INDEX.md
  - Central index of documentation with 1-line purposes; includes governance/community-health docs and GitHub meta files.
- .github/CODEOWNERS
  - Code ownership rules to route reviews and enforce ownership boundaries.
- .github/dependabot.yml
  - Dependency update configuration for automated PRs.
- .github/pull_request_template.md
  - PR checklist emphasizing frozen boundaries (no engine/template/contract/golden/manifest drift).
- .github/ISSUE_TEMPLATE/config.yml
  - Issue intake routing / links to support + FAQ.
- .github/ISSUE_TEMPLATE/bug_report.md
  - Bug template with reproducibility + environment fields (including install source: tag/main/commit SHA).
- .github/ISSUE_TEMPLATE/feature_request.md
  - Feature request template that sets expectations against frozen surfaces.

### Added (repo scaffolding)
- .gitattributes — Line-ending/text normalization for cross-platform stability.
- .gitignore — Ignore local/ephemeral artifacts to keep commits clean.
- _hashcheck.py — Local helper for manifest hash verification.
- BACKLOG.md — Backlog tracking for future work/triage.
- MANIFEST.in — Packaging rules for including required non-code artifacts.

### Notes
- Docs/repo-governance only: no engine code, templates, API contract, SDT semantics, golden cases, CI behavior, or package behavior changes.


## v1.0.1

- R01 — Template pack builder hardening (md → json).
- R02 — Documentation clarity: integrity gate vs SDT gate separation.
- R03 — Windows env-var parity command block standardization.
- R04 — Test runner parity: explicit unittest list vs discovery.
- R05 — CI hygiene tightening.

## v1.0.0

MicroInX v1.0.0 freezes a deterministic micro-insight engine that maps minimal user text into a single BladeInsight using a fixed five-vector model and a frozen 15-template surface, with release integrity enforced via manifest hash verification, template fidelity enforced via exact canonical template matching, and SDT enforcing forbidden-token bans (and other SDT rule checks).

Included packs:
- Release Candidate Pack (v1.0)
- Integration Adapter Pack (v1.0)
- API Contract Pack (v1.0)
- One-Command Demo Pack (v1.0)
- Distribution Pack (v1.0)
- CI Smoke Pack (v1.0)
- Golden Regression Pack (v1.0)
- Repo Index Pack (v1.0)

Behavioral invariants:
- Determinism: identical input text yields identical `{template_id, output_text, sdt}`.
- Manifest integrity refusal: runtime/serve path refuses when any required file hash mismatches the release manifest.
- SDT gate: outputs fail SDT on forbidden tokens, interrogatives, emoji/emoticons, or length violations.
- Template fidelity: selected `template_id` maps to an exact canonical template string (exact-match enforcement).

No behavior change; golden outputs unchanged.