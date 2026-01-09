# src/manifestinx/template_pack_builder.py
# Manifest-InX v1.0.0
#
# Deterministic template pack builder (v0.3 → templates_v0_3.json).
#
# Constraints:
# - No mapping changes, no template text changes.
# - Canonical output for the canonical markdown source must be byte-identical to
#   the committed src/manifestinx/data/templates_v0_3.json.
# - Robust to trivial formatting variance in the markdown (e.g., bullet prefix
#   or extra whitespace), without changing extracted template texts.

from __future__ import annotations

import json
import re
from typing import Dict


# Accept optional bullet prefix and extra whitespace. Canonical line shape:
#   **T01** [drift] — <template text>
# We extract the template text after the first dash-like separator.
_LINE_RE = re.compile(r"^\s*(?:[-*]|\d+\.)?\s*\*\*(T\d{2})\*\*.*?[—–-]\s*(.+?)\s*$")


def parse_template_library_markdown(md_text: str) -> Dict[str, str]:
    """Parse a v0.3 template markdown string into {template_id: text}.

    Robustness policy:
    - Ignores trivial leading bullets ("-", "*", "1.") and extra whitespace.
    - Accepts em dash (—), en dash (–), or hyphen (-) as the separator.
    - Template text is trimmed at both ends, but otherwise preserved verbatim.

    Raises:
      ValueError if no templates are found.
    """
    out: Dict[str, str] = {}
    for line in md_text.splitlines():
        m = _LINE_RE.match(line)
        if not m:
            continue
        tid, text = m.group(1), m.group(2).strip()
        out[tid] = text

    if not out:
        raise ValueError("no templates found in markdown")
    return out


def build_templates_json_bytes(mapping: Dict[str, str], newline: str = "\n") -> bytes:
    """Deterministically serialize {template_id: text} as JSON bytes.

    Notes:
    - We force LF by default to match the repository's frozen pack bytes.
    - We always end with exactly one trailing newline.
    """
    s = json.dumps(mapping, ensure_ascii=False, sort_keys=True, indent=2)
    s = s.replace("\n", newline) + newline
    return s.encode("utf-8")


def build_templates_v0_3_json_bytes_from_markdown(md_text: str, newline: str = "\n") -> bytes:
    """Convenience: parse markdown and emit templates_v0_3.json bytes."""
    m = parse_template_library_markdown(md_text)
    return build_templates_json_bytes(m, newline=newline)