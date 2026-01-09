# src/inxzap/compat.py
# Step 3: compatibility entrypoint (do not alter stdout JSON)

from __future__ import annotations

import sys

from inxzap import demo as _inxzap_demo


def manifestinx_demo_main() -> int:
    # One line. No empathy. No narrative. STDERR only.
    print("DEPRECATED: manifestinx-demo -> use inxzap-demo", file=sys.stderr)
    return _inxzap_demo.main()
