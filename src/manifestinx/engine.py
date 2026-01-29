# src/manifestinx/engine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

from pathlib import Path
from .pack_system import PackHandle, ValidationReport, load_pack as _load_pack, validate_pack as _validate_pack

import hashlib

# Core MUST be domain-agnostic:
# - No product taxonomy (drift/avoidance/...)
# - No implied template catalog (T01..T15)
#
# We keep a deterministic feature vector as a core primitive.
FEATURE_DIMS: tuple[str, ...] = ("d01", "d02", "d03", "d04", "d05")


@dataclass(frozen=True)
class CoreResult:
    ok: bool
    input_text: str
    # Deterministic, stable ordering
    feature_dim_order: tuple[str, ...]
    feature_vector: tuple[float, ...]
    dominant_dim: str
    # Optional pack-defined identifier; core does not compute this
    pack_identifier: Optional[str] = None
    diagnostics: Optional[Mapping[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "ok": self.ok,
            "input_text": self.input_text,
            "feature_dim_order": list(self.feature_dim_order),
            "feature_vector": list(self.feature_vector),
            "dominant_dim": self.dominant_dim,
        }
        if self.pack_identifier is not None:
            out["pack_identifier"] = self.pack_identifier
        if self.diagnostics is not None:
            out["diagnostics"] = dict(self.diagnostics)
        return out


class Engine:
    """
    v2.0.1 core-only engine.

    Core responsibilities:
    - deterministic canonicalization (if present elsewhere in your codebase)
    - deterministic feature extraction (domain-agnostic)
    - pack loading/validation via Pack System v0.1 (handled in engine facade or pack_system module)

    Core explicitly does NOT:
    - ship templates
    - assume a template catalog
    - map to product template IDs
    """

    def __init__(self) -> None:
        # If you already have more init state, keep it.
        pass

    # ---- pack-system façade (v0.1 local-only) ----

    def validate_pack(self, path: str | Path) -> ValidationReport:
        return _validate_pack(path)

    def load_pack(self, path: str | Path) -> PackHandle:
        return _load_pack(path)

    # ---- core deterministic feature extraction ----

    def run_text(self, text: str, *, diagnostics: bool = False) -> dict[str, Any]:
        """
        Deterministically convert input text into a domain-agnostic feature vector.

        NOTE:
        - No template_id is produced by core.
        - Any mapping to pack-specific identifiers must be performed by pack-defined pipeline logic.
        """
        input_text = text if isinstance(text, str) else str(text)

        vec = self._compute_feature_vector(input_text)
        dominant_idx = max(range(len(vec)), key=lambda i: vec[i])
        dominant_dim = FEATURE_DIMS[dominant_idx]

        diag: Optional[dict[str, Any]] = None
        if diagnostics:
            diag = {
                "feature_dim_count": len(FEATURE_DIMS),
                "dominant_index": dominant_idx,
            }

        result = CoreResult(
            ok=True,
            input_text=input_text,
            feature_dim_order=FEATURE_DIMS,
            feature_vector=tuple(vec),
            dominant_dim=dominant_dim,
            diagnostics=diag,
        )
        return result.to_dict()

    def _compute_feature_vector(self, input_text: str) -> Sequence[float]:
        """
        Deterministic, domain-agnostic feature vector.

        Uses sha256 over raw UTF-8 bytes of the input text and converts the digest
        into a fixed-length numeric vector in a stable way.

        - No product taxonomy
        - No template mapping
        - No external deps
        """
        b = input_text.encode("utf-8")
        digest = hashlib.sha256(b).digest()  # 32 bytes

        # Turn digest into 5 stable dimensions using 4-byte chunks.
        # (20 bytes used, leaving the remainder unused by design.)
        vals = []
        for i in range(5):
            chunk = digest[i * 4 : (i + 1) * 4]
            n = int.from_bytes(chunk, "big", signed=False)
            vals.append(n)

        total = sum(vals)
        if total == 0:
            return [0.0] * 5

        # Normalize to a probability-like vector for stable downstream use
        return [v / total for v in vals]
        # ---- END ----
