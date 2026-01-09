# src/inxzap/demo.py
# Step 2: delegate to manifestinx.demo:main

from __future__ import annotations

from manifestinx import demo as _engine_demo


def main() -> int:
    return _engine_demo.main()


if __name__ == "__main__":
    raise SystemExit(main())
