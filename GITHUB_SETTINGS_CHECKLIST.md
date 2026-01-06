# GITHUB_SETTINGS_CHECKLIST.md

Single-page, UI-executable checklist to protect the frozen MicroInX v1.0.2 surface.

---

## 1) Default branch

- **Settings → Branches → Default branch**
  - Default branch: **main**

---

## 2) Branch protection for `main`

Path: **Settings → Branches → Branch protection rules → Add rule**

- **Branch name pattern**: `main`

### Pull request requirements

- Enable **Require a pull request before merging**
  - Enable **Require approvals**: `1`
  - Enable **Dismiss stale pull request approvals when new commits are pushed**
  - (Optional) Enable **Require review from Code Owners** *(requires a `CODEOWNERS` file)*

### Status checks

- Enable **Require status checks to pass before merging**
  - Enable **Require branches to be up to date before merging** *(optional; higher friction)*
  - Select the exact checks produced by `.github/workflows/microinx_ci.yml`:
    - Workflow: `microinx-ci`
    - Required check runs (matrix):
      - `smoke (3.10)`
      - `smoke (3.12)`

### Protections against history rewrite

- Enable **Require linear history** *(optional; pairs well with squash-only)*
- Enable **Prevent force pushes**
- Enable **Prevent deletions**

### Bypass / admin controls

- Keep bypass access minimal.
  - If available, enable **Do not allow bypassing the above settings** (or restrict bypass to repo admins only).

---

## 3) Merge policy

Path: **Settings → General → Pull Requests**

- Enable **Allow squash merging**
  - Set default commit message style to match your release discipline (any is fine).
- Disable **Allow merge commits** *(optional; reduces history branching)*
- Disable **Allow rebase merging** *(optional; keep one merge mode)*
- If **Require linear history** was enabled in branch protection, keep it consistent with the merge options above.

---

## 4) Releases and tag protection

Path: **Settings → Tags → Tag protection rules → Add rule** *(UI may vary by plan/org)*

- Add a tag protection rule:
  - **Pattern**: `v*`
  - Restrict tag creation/deletion to maintainers only (if the UI supports it)

---

## 5) Security toggles

Path: **Settings → Security & analysis** *(UI labels may vary)*

Enable the following if available:

- **Private vulnerability reporting**
- **Security advisories**
- **Dependency graph**
- **Dependabot alerts**
- (Optional) **Dependabot security updates** *(auto PRs; adds some noise)*

---

## 6) Issues and PRs

### Issue templates

Path: **Settings → General → Features** *(and/or)* **Issues → New issue**

- Ensure **Issues** are enabled.
- Ensure issue templates are active (repo includes `.github/ISSUE_TEMPLATE/*`).

### Pull request template

- Ensure PRs are enabled.
- Confirm the PR template renders when opening a PR (`.github/pull_request_template.md`).