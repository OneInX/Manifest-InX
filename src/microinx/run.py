# run.py
# MicroInX Release Candidate Entrypoint v1.0.0 (Sprint 3)
#
# Deterministic callable + minimal CLI wrapper.
# Refuses to run if release hash manifest verification fails.

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from importlib import resources as ir


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


MANIFEST_PATH = Path(os.environ.get("MICROINX_MANIFEST_PATH", "microinx_manifest_v1.json"))


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_release(manifest_path: Path = MANIFEST_PATH, base_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Verify frozen release hashes.

    Raises:
        RuntimeError: if any listed file hash mismatches or files are missing.

    Returns:
        The parsed manifest dict.
    """
    base_dir = base_dir or Path.cwd()
    mpath = manifest_path if manifest_path.is_absolute() else (base_dir / manifest_path)
    if not mpath.exists():
        raise RuntimeError(f"release manifest missing: {mpath.name}")

    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    files = manifest.get("files", {})
    if not isinstance(files, dict) or not files:
        raise RuntimeError("release manifest invalid: missing 'files'")

    for rel, expected in files.items():
        fpath = Path(rel)
        fpath = fpath if fpath.is_absolute() else (base_dir / fpath)
        if not fpath.exists():
            raise RuntimeError(f"release file missing: {Path(rel).name}")
        got = _sha256_hex(fpath.read_bytes())
        if got != expected:
            raise RuntimeError(f"release hash mismatch: {Path(rel).name}")

    return manifest


def microinx_run(text: str, lang: str = "auto", source: str = "chat") -> Dict[str, Any]:
    """Stable deterministic entrypoint.

    Public API intentionally excludes any time parameter to reduce surface area; scoring is input-only.
    """
    verify_release()

    import microinx.engine as engine  # local stable engine module

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
    p.add_argument("text", help="Input text (1–2000 chars)")
    p.add_argument("--json", action="store_true", help="Emit JSON {template_id, output_text, sdt}")
    p.add_argument("--lang", default="auto", help="en|ko|auto (default: auto)")
    p.add_argument("--source", default="chat", help="chat|note|other (default: chat)")
    args = p.parse_args(argv)

    try:
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
