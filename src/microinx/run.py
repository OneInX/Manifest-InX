# src/microinx/run.py
# MicroInX Release Candidate Entrypoint v1.0.x.
#
# Deterministic callable + minimal CLI wrapper.
# Refuses to run if release hash manifest verification fails.
#
# Supports BOTH:
# - repo layout (files on disk under src/microinx/...)
# - installed package layout (data loaded via importlib.resources)

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from importlib import resources as ir

DEFAULT_MANIFEST_BASENAME = "microinx_manifest_v1.json"

def _read_bytes_cwd_or_pkg(filename: str) -> bytes:
    p = Path(filename)
    if p.is_file():
        return p.read_bytes()
    # packaged fallback: microinx/data/<filename>
    try:
        return (ir.files("microinx") / "data" / filename).read_bytes()
    except Exception as e:
        raise FileNotFoundError(
            f"Missing {filename}: not found in CWD and not found in package data microinx/data/"
        ) from e


def _read_json_cwd_or_pkg(filename: str):
    return json.loads(_read_bytes_cwd_or_pkg(filename).decode("utf-8"))


# Then, in the existing loaders (examples; keep existing variable names / logic):
# - Wherever templates_v0_3.json is loaded:
#     templates = _read_json_cwd_or_pkg("templates_v0_3.json")
# - Wherever microinx_manifest_v1.json is loaded:
#     manifest = _read_json_cwd_or_pkg("microinx_manifest_v1.json")
# - Wherever hashes are computed over the manifest/template bytes, use _read_bytes_cwd_or_pkg(...)


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_manifest_bytes(base_dir: Path, manifest_path: Optional[str]) -> Tuple[bytes, str]:
    """
    Returns: (bytes, origin_label)
    Search order:
      1) explicit manifest_path (file system)
      2) env MICROINX_MANIFEST_PATH (file system)
      3) repo-style: <base_dir>/microinx_manifest_v1.json
      4) package data: microinx.data/microinx_manifest_v1.json
    """
    candidate = manifest_path or os.environ.get("MICROINX_MANIFEST_PATH")

    if candidate:
        p = Path(candidate)
        if not p.is_absolute():
            p = base_dir / p
        if not p.exists():
            raise RuntimeError(f"release manifest missing: {p.name}")
        return (p.read_bytes(), f"fs:{p}")

    # repo-root convenience (optional)
    p = base_dir / DEFAULT_MANIFEST_BASENAME
    if p.exists():
        return (p.read_bytes(), f"fs:{p}")

    # installed package data
    try:
        b = ir.files("microinx.data").joinpath(DEFAULT_MANIFEST_BASENAME).read_bytes()
        return (b, "pkg:microinx.data/" + DEFAULT_MANIFEST_BASENAME)
    except Exception as e:
        raise RuntimeError("release manifest missing: microinx.data/microinx_manifest_v1.json") from e


def _read_bytes_for_manifest_key(base_dir: Path, key: str) -> bytes:
    """
    Manifest keys are package-relative, expected to include:
      - 'run.py'
      - 'engine.py'
      - 'data/templates_v0_3.json'
    Resolution order per key:
      1) file system (repo-style): <base_dir>/src/microinx/<key>
      2) file system (flat): <base_dir>/<key>
      3) package resources:
         - if key starts with 'data/': microinx.data/<basename>
         - else: microinx/<key>
    """
    # repo-style under src/
    repo_style = base_dir / "src" / "microinx" / key
    if repo_style.exists():
        return repo_style.read_bytes()

    # flat path (for ad-hoc layouts)
    flat = base_dir / key
    if flat.exists():
        return flat.read_bytes()

    # package resource lookup
    try:
        if key.startswith("data/"):
            name = key[len("data/") :]
            return ir.files("microinx.data").joinpath(name).read_bytes()
        return ir.files("microinx").joinpath(key).read_bytes()
    except Exception as e:
        raise RuntimeError(f"release file missing: {Path(key).name}") from e


def verify_release(manifest_path: Optional[str] = None, base_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Verify frozen release hashes.

    Raises:
        RuntimeError: if any listed file hash mismatches or files are missing.

    Returns:
        Parsed manifest dict.
    """
    base_dir = base_dir or Path.cwd()

    manifest_bytes, _origin = _load_manifest_bytes(base_dir, manifest_path)
    manifest = json.loads(manifest_bytes.decode("utf-8"))

    files = manifest.get("files", {})
    if not isinstance(files, dict) or not files:
        raise RuntimeError("release manifest invalid: missing 'files'")

    for key, expected in files.items():
        if not isinstance(expected, str) or len(expected) != 64:
            raise RuntimeError(f"release manifest invalid hash for: {key}")
        got = _sha256_hex(_read_bytes_for_manifest_key(base_dir, key))
        if got != expected:
            raise RuntimeError(f"release hash mismatch: {Path(key).name}")

    return manifest


def compute_release_hashes(base_dir: Optional[Path] = None) -> Dict[str, str]:
    """Utility for regenerating hashes after file moves/edits (not used in runtime logic)."""
    base_dir = base_dir or Path.cwd()
    keys = ["run.py", "engine.py", "data/templates_v0_3.json"]
    out: Dict[str, str] = {}
    for k in keys:
        out[k] = _sha256_hex(_read_bytes_for_manifest_key(base_dir, k))
    return out


def microinx_run(text: str, lang: str = "auto", source: str = "chat") -> Dict[str, Any]:
    """Stable deterministic entrypoint.

    Public API intentionally excludes any time parameter to reduce surface area; scoring is input-only.
    """
    verify_release()

    # local package module
    from . import engine

    minimal_user_signal = {
        "raw_text": text,
        "lang": lang,
        "source": source,
    }
    res = engine.generate_blade_insight(minimal_user_signal)
    return {
        "template_id": res["template_id"],
        "output_text": res["output_text"],
        "sdt": res["sdt"],
    }


def _main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="microinx", add_help=True)
    p.add_argument("text", nargs="?", help="Input text (1–2000 chars)")
    p.add_argument("--json", action="store_true", help="Emit JSON {template_id, output_text, sdt}")
    p.add_argument("--lang", default="auto", help="en|ko|auto (default: auto)")
    p.add_argument("--source", default="chat", help="chat|note|other (default: chat)")
    p.add_argument("--verify-only", action="store_true", help="Only verify release manifest and exit")
    p.add_argument("--print-hashes", action="store_true", help="Print expected sha256 map for current files and exit")
    args = p.parse_args(argv)

    try:
        if args.print_hashes:
            print(json.dumps(compute_release_hashes(), sort_keys=True))
            return 0

        if args.verify_only:
            verify_release()
            print("OK")
            return 0

        if not args.text:
            p.error("text is required unless --verify-only or --print-hashes is used")

        out = microinx_run(args.text, lang=args.lang, source=args.source)

    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    else:
        print(out["output_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
