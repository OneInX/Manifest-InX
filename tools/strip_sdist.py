"""Strip build debris from an sdist tar.gz.

Policy: remove any *.egg-info/ entries (and their children) from the sdist.

This is a lightweight post-process step to keep release artifacts clean without
changing the build backend.
"""

from __future__ import annotations

import argparse
import io
import os
import tarfile
from pathlib import Path


def strip_sdist(path: Path) -> None:
    src = path
    tmp = path.with_suffix(path.suffix + ".tmp")

    with tarfile.open(src, "r:gz") as tf_in, tarfile.open(tmp, "w:gz") as tf_out:
        for m in tf_in.getmembers():
            name = m.name
            if ".egg-info/" in name:
                continue
            if name.endswith(".egg-info"):
                continue
            f = tf_in.extractfile(m) if m.isfile() else None
            tf_out.addfile(m, f)

    os.replace(tmp, src)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sdist", help="Path to sdist tar.gz")
    args = ap.parse_args(argv)
    strip_sdist(Path(args.sdist))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
