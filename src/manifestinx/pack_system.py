"""Pack System v0.1 (local-path only).

Core goals:
- Deterministic, auditable: sha256 pins over raw file bytes.
- No network loading.
- Read-only pack handle after validation.

Pack layout:
- <pack_root>/pack_manifest.json
- referenced files under <pack_root>/...

The manifest schema file ships at:
- manifestinx/schemas/pack_manifest_v0_1.json

Validation in v0.1:
- Enforces required keys + types.
- Validates relpath safety (no absolute, no traversal, no drive letters).
- Validates sha256 pins (raw bytes).
- Future-proofing fields are validated for type/format only:
  - version
  - engine_compat.min_version / engine_compat.max_version

No network loading in v0.1.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping


_SHA256_HEX_RE = re.compile(r"^[a-f0-9]{64}$")
_SEMVER_LIKE_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+([\-\+][A-Za-z0-9.\-]+)?$")


class PackValidationError(RuntimeError):
    """Raised when attempting to load a pack that fails validation."""


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = {"code": self.code, "message": self.message}
        if self.path is not None:
            d["path"] = self.path
        return d


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    issues: tuple[ValidationIssue, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "issues": [i.to_dict() for i in self.issues]}


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _is_safe_relpath(p: str) -> bool:
    """Relpath safety rules for v0.1.

    - must be relative
    - no '..' segments
    - no Windows drive letters
    - no backslashes
    - no leading '/'
    """
    if not isinstance(p, str) or not p:
        return False
    if p.startswith("/"):
        return False
    if "\\" in p:
        return False
    if re.match(r"^[A-Za-z]:", p):
        return False
    parts = [x for x in p.split("/") if x]
    if any(x == ".." for x in parts):
        return False
    return True


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest(pack_root: Path) -> MutableMapping[str, Any]:
    mf = pack_root / "pack_manifest.json"
    if not mf.exists() or not mf.is_file():
        raise FileNotFoundError(f"Missing pack_manifest.json at: {mf}")
    obj = _read_json(mf)
    if not isinstance(obj, dict):
        raise ValueError("pack_manifest.json must be a JSON object")
    return obj


def validate_pack(pack_root: str | Path) -> ValidationReport:
    root = Path(pack_root).expanduser().resolve()
    issues: list[ValidationIssue] = []

    try:
        manifest = _load_manifest(root)
    except Exception as e:
        return ValidationReport(False, (ValidationIssue("MANIFEST_READ_ERROR", str(e), "pack_manifest.json"),))

    # Required fields
    schema_version = manifest.get("schema_version")
    if schema_version != "pack_manifest_v0.1":
        issues.append(
            ValidationIssue(
                "SCHEMA_VERSION",
                "schema_version must equal 'pack_manifest_v0.1'",
                "schema_version",
            )
        )

    pack_id = manifest.get("pack_id")
    if not isinstance(pack_id, str) or not pack_id.strip():
        issues.append(ValidationIssue("PACK_ID", "pack_id must be a non-empty string", "pack_id"))

    # Optional future-proofing fields (format/type only)
    version = manifest.get("version")
    if version is not None:
        if not isinstance(version, str) or not _SEMVER_LIKE_RE.match(version):
            issues.append(
                ValidationIssue(
                    "VERSION_FORMAT",
                    "version must be a SemVer-like string (e.g., 1.2.3 or 1.2.3-rc.1)",
                    "version",
                )
            )

    engine_compat = manifest.get("engine_compat")
    if engine_compat is not None:
        if not isinstance(engine_compat, dict):
            issues.append(
                ValidationIssue(
                    "ENGINE_COMPAT_TYPE",
                    "engine_compat must be an object",
                    "engine_compat",
                )
            )
        else:
            for k in ("min_version", "max_version"):
                v = engine_compat.get(k)
                if v is None:
                    continue
                if not isinstance(v, str) or not _SEMVER_LIKE_RE.match(v):
                    issues.append(
                        ValidationIssue(
                            "ENGINE_COMPAT_FORMAT",
                            f"engine_compat.{k} must be a SemVer-like string",
                            f"engine_compat.{k}",
                        )
                    )

    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        issues.append(ValidationIssue("FILES", "files must be a non-empty object mapping relpath -> sha256", "files"))
        return ValidationReport(False, tuple(issues))

    # Validate file pins
    for relpath, sha in files.items():
        if not isinstance(relpath, str) or not _is_safe_relpath(relpath):
            issues.append(ValidationIssue("PATH_UNSAFE", "file path must be a safe relative path", str(relpath)))
            continue
        if not isinstance(sha, str) or not _SHA256_HEX_RE.match(sha):
            issues.append(ValidationIssue("SHA256_FORMAT", "sha256 must be 64 lowercase hex chars", relpath))
            continue

        fpath = (root / relpath).resolve()
        # Ensure path stays within pack root
        try:
            fpath.relative_to(root)
        except Exception:
            issues.append(ValidationIssue("PATH_TRAVERSAL", "file resolves outside pack root", relpath))
            continue

        if not fpath.exists() or not fpath.is_file():
            issues.append(ValidationIssue("FILE_MISSING", "pinned file missing", relpath))
            continue

        raw = fpath.read_bytes()
        got = _sha256_hex(raw)
        if got != sha:
            issues.append(
                ValidationIssue(
                    "SHA256_MISMATCH",
                    "sha256 pin mismatch for raw bytes",
                    relpath,
                )
            )

    # Entrypoints
    entrypoints = manifest.get("entrypoints")
    if entrypoints is not None:
        if not isinstance(entrypoints, dict):
            issues.append(ValidationIssue("ENTRYPOINTS_TYPE", "entrypoints must be an object", "entrypoints"))
        else:
            for name, rel in entrypoints.items():
                if not isinstance(name, str) or not name:
                    issues.append(ValidationIssue("ENTRYPOINT_NAME", "entrypoint name must be a non-empty string", "entrypoints"))
                    continue
                if not isinstance(rel, str) or not _is_safe_relpath(rel):
                    issues.append(ValidationIssue("ENTRYPOINT_PATH", "entrypoint relpath must be a safe relative path", f"entrypoints.{name}"))
                    continue
                if rel not in files:
                    issues.append(ValidationIssue("ENTRYPOINT_NOT_PINNED", "entrypoint must reference a pinned file in files", f"entrypoints.{name}"))

    return ValidationReport(ok=(len(issues) == 0), issues=tuple(issues))


@dataclass(frozen=True)
class PackHandle:
    """Read-only handle to a validated pack."""

    root: Path
    manifest: Mapping[str, Any]

    def entrypoint_path(self, name: str) -> Path:
        eps = self.manifest.get("entrypoints") or {}
        if not isinstance(eps, dict) or name not in eps:
            raise KeyError(f"Unknown entrypoint: {name}")
        rel = eps[name]
        if not isinstance(rel, str) or not _is_safe_relpath(rel):
            raise ValueError(f"Unsafe entrypoint path for {name}")
        p = (self.root / rel).resolve()
        p.relative_to(self.root)
        return p

    def read_bytes(self, relpath: str) -> bytes:
        if not _is_safe_relpath(relpath):
            raise ValueError("Unsafe relpath")
        p = (self.root / relpath).resolve()
        p.relative_to(self.root)
        return p.read_bytes()

    def read_text(self, relpath: str, encoding: str = "utf-8") -> str:
        return self.read_bytes(relpath).decode(encoding)

    def read_json(self, relpath: str) -> Any:
        return json.loads(self.read_text(relpath, encoding="utf-8"))


def load_pack(pack_root: str | Path) -> PackHandle:
    root = Path(pack_root).expanduser().resolve()
    report = validate_pack(root)
    if not report.ok:
        # Deterministic error message ordering
        msg = "; ".join(f"{i.code}:{i.path or ''}" for i in report.issues)
        raise PackValidationError(f"Pack validation failed: {msg}")

    manifest = _load_manifest(root)
    return PackHandle(root=root, manifest=manifest)
