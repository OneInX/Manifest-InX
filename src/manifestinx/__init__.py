"""Manifest-InX core package (v2.0.0).

Public surface (core-only):
- Engine (domain-agnostic deterministic core)
- Pack System v0.1 helpers (local path load + sha256 pin validation)

Core does not ship templates, packs, or product taxonomies.
"""

from __future__ import annotations

from .engine import Engine
from .pack_system import (
    PackHandle,
    ValidationIssue,
    ValidationReport,
    load_pack,
    validate_pack,
)

__all__ = [
    "Engine",
    "PackHandle",
    "ValidationIssue",
    "ValidationReport",
    "validate_pack",
    "load_pack",
]
