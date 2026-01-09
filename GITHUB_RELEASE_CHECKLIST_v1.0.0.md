# GITHUB_RELEASE_CHECKLIST_v1.0.0 — Manifest-InX

Executable checklist for publishing **Manifest-InX v1.0.0** (engine: `manifestinx`, reference wrapper: `inxzap`).

Scope: release hygiene only. No template/SDT/contract/golden behavior changes.

---

## 0) Preconditions

- Working tree clean:
  - `git status`
- You are on the intended branch:
  - `git branch --show-current`
- Canonical names present:
  - Engine: `src/manifestinx/`
  - Wrapper: `src/inxzap/`
  - CLI: `inxzap-demo`
  - Demo env var: `MANIFESTINX_DEMO_PORT`
- Contract filename aligned:
  - `openapi_manifestinx_v1.yaml`

---

## 1) Docs/structure sanity

- `README.md` quickstart uses:
  - PowerShell: `$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo`
- `DOCS_INDEX.md` references the correct workflow filename and test commands.
- `DEMO.md` is pack-branded (`inxzap-demo`) and uses `MANIFESTINX_DEMO_PORT`.
- `GOLDEN.md` points to:
  - `src/manifestinx/data/golden_cases_v1.json`
- `CHANGELOG.md` includes a **v1.0.0** section for Manifest-InX.

---

## 2) Full test verification (local)

### Windows PowerShell

- Demo smoke (ephemeral port):
  - `$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo`

- Full suite (recommended):
  - `python -m unittest discover -s tests -v`

- CI parity (explicit):
  - `python -m unittest -q tests.test_manifestinx_engine`
  - `python -m unittest -q tests.test_manifestinx_api_smoke`
  - `python -m unittest -q tests.test_manifestinx_api_contract`
  - `python -m unittest -q tests.test_manifestinx_demo_smoke`
  - `python -m unittest -q tests.test_manifestinx_golden_regression`

### Bash

- Demo smoke:
  - `MANIFESTINX_DEMO_PORT=0 inxzap-demo`

- Full suite:
  - `python -m unittest discover -s tests -v`

Gate: all PASS.

---

## 3) Build artifacts (sdist + wheel)

Install build tooling if needed:

- `python -m pip install -U build twine`

Build:

- `python -m build`

Check metadata:

- `python -m twine check dist/*`

Gate: twine check PASS.

---

## 4) Sdist contents sanity (required)

Verify the sdist contains required data/docs.

### Cross-platform (Python)

Run from repo root:

```bash
python - <<'PY'
import glob, tarfile
paths = glob.glob('dist/*.tar.gz')
assert paths, 'No sdist found in dist/*.tar.gz'
path = paths[0]
need = [
  'openapi_manifestinx_v1.yaml',
  'MANIFEST.in',
  'src/manifestinx/data/manifestinx_manifest_v1.json',
  'src/manifestinx/data/templates_v0_3.json',
  'src/manifestinx/data/golden_cases_v1.json',
]
with tarfile.open(path, 'r:gz') as tf:
  names = tf.getnames()
  missing = []
  for n in need:
    if not any(x.endswith('/'+n) or x == n for x in names):
      missing.append(n)
print('sdist:', path)
if missing:
  raise SystemExit('MISSING in sdist: ' + ', '.join(missing))
print('sdist contents: OK')
PY
```

Gate: sdist contents OK.

---

## 5) Version + tag

Ensure pyproject.toml:

- `name = "manifestinx"`

- `version = "1.0.0"`

Commit any final doc/link adjustments:

- `git add -A`

- `git commit -m "Manifest-InX v1.0.0"`

Create annotated tag:

- `git tag -a v1.0.0 -m "Manifest-InX v1.0.0"`

Gate: `git tag -l "v1.0.0"` shows the tag.

---

## 6) Push to new GitHub repo

Create repo: `OneInX/Manifest-InX` (GitHub UI).

Add remote (example):

- `git remote add manifest https://github.com/OneInX/Manifest-InX.git`

Push:

- `git push manifest main --follow-tags`

- `git push manifest v1.0.0`

Gate: tag visible on GitHub.

---

## 7) GitHub Actions CI verification

- Trigger CI on `main` (push already triggers it).

- Confirm all matrix jobs pass.

Then update GITHUB_SETTINGS_CHECKLIST.md with the exact required check names as they appear in GitHub (often includes matrix suffixes).

Gate: CI green on `main`.

---

## 8) Create GitHub Release (v1.0.0)

- Create a GitHub Release from tag `v1.0.0`.

- Release title: `Manifest-InX v1.0.0`

- Release notes must include:

    - what is frozen (templates/SDT/contract/golden/manifest refusal)

    - primary demo entrypoint: `inxzap-demo`

    - demo env var: `MANIFESTINX_DEMO_PORT`

    - build artifacts attached (wheel + sdist)

---

## 9) Post-release quick recheck

- Fresh venv install from the repo tag (local):

    - `python -m pip install -e . --no-deps`

- Run:

    - `$env:MANIFESTINX_DEMO_PORT=0; inxzap-demo`

Gate: demo prints JSON with `manifest.hash_ok: true.`