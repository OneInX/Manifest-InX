"""Repo + release artifact lint for Manifest-InX core-only policy.

Fails if:
- Forbidden paths are tracked in git index (if .git available).
- Forbidden files/paths appear in wheel or sdist artifacts.

Intended to run in CI.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path


FORBIDDEN_TRACKED_PATTERNS = [
    r"^src/inxzap/",
    r"^src/manifestinx/data/",
    r"^dist/",
    r"^build/",
    r"^\.venv/",
    r"__pycache__",
    r"\.egg-info/",
]

FORBIDDEN_ARTIFACT_SUBSTRINGS = [
    "inxzap",
    "manifestinx/data",
    "templates_v0_",
    "__pycache__",
    ".egg-info",
]


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def _git_ls_files(repo_root: Path) -> list[str]:
    if not (repo_root / ".git").exists():
        return []
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=str(repo_root))
    except Exception as e:
        _fail(f"git ls-files failed: {e}")
    return [ln.strip() for ln in out.decode("utf-8", errors="replace").splitlines() if ln.strip()]


def lint_tracked(repo_root: Path) -> None:
    tracked = _git_ls_files(repo_root)
    if not tracked:
        return

    bad: list[str] = []
    for p in tracked:
        for pat in FORBIDDEN_TRACKED_PATTERNS:
            if re.search(pat, p):
                bad.append(p)
                break
    if bad:
        _fail("Forbidden tracked paths detected:\n" + "\n".join(f"- {b}" for b in sorted(set(bad))))


def lint_wheel(wheel_path: Path) -> None:
    with zipfile.ZipFile(wheel_path, "r") as z:
        names = z.namelist()

    # Forbidden substring scan
    bad = [n for n in names if any(s in n for s in FORBIDDEN_ARTIFACT_SUBSTRINGS)]
    if bad:
        _fail(f"Forbidden content in wheel {wheel_path.name}:\n" + "\n".join(f"- {b}" for b in sorted(set(bad))))

    # Core-only: only manifestinx/ + dist-info
    allowed_prefixes = ("manifestinx/",)
    distinfo_re = re.compile(r"^manifestinx-.*\.dist-info/")
    for n in names:
        if n.endswith("/"):
            continue
        if n.startswith(allowed_prefixes):
            continue
        if distinfo_re.search(n):
            continue
        _fail(f"Unexpected wheel file outside core surface: {n}")


def lint_sdist(sdist_path: Path) -> None:
    with tarfile.open(sdist_path, "r:gz") as tf:
        members = [m.name for m in tf.getmembers()]

    bad = [n for n in members if any(s in n for s in FORBIDDEN_ARTIFACT_SUBSTRINGS)]
    if bad:
        _fail(f"Forbidden content in sdist {sdist_path.name}:\n" + "\n".join(f"- {b}" for b in sorted(set(bad))))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="Repo root")
    ap.add_argument("--artifacts", default="dist", help="Artifacts directory")
    args = ap.parse_args(argv)

    repo_root = Path(args.repo).resolve()
    dist_dir = Path(args.artifacts).resolve()

    lint_tracked(repo_root)

    if dist_dir.exists():
        wheels = sorted(dist_dir.glob("*.whl"))
        sdists = sorted(dist_dir.glob("*.tar.gz"))
        if not wheels or not sdists:
            _fail(f"Expected both wheel and sdist in {dist_dir}")
        for w in wheels:
            lint_wheel(w)
        for s in sdists:
            lint_sdist(s)

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
