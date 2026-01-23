"""Manifest-InX core CLI.

This CLI is intentionally minimal and core-focused.

Commands:
- manifestinx --help
- manifestinx pack validate <path>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .pack_system import validate_pack


def _cmd_pack_validate(args: argparse.Namespace) -> int:
    report = validate_pack(Path(args.path))
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        if report.ok:
            print("OK")
        else:
            print("FAIL")
            for issue in report.issues:
                loc = f" [{issue.path}]" if issue.path else ""
                print(f"- {issue.code}{loc}: {issue.message}")
    return 0 if report.ok else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="manifestinx")
    sub = p.add_subparsers(dest="cmd")

    pack = sub.add_parser("pack", help="Pack system utilities")
    pack_sub = pack.add_subparsers(dest="pack_cmd")

    v = pack_sub.add_parser("validate", help="Validate a local pack")
    v.add_argument("path", help="Path to pack root directory")
    v.add_argument("--json", action="store_true", help="Emit JSON report")
    v.set_defaults(_fn=_cmd_pack_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    fn = getattr(args, "_fn", None)
    if fn is None:
        # If no subcommand chosen, show help.
        parser.print_help()
        return 0
    return int(fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
