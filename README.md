# Manifest-InX

[![CI](https://github.com/OneInX/Manifest-InX/actions/workflows/manifestinx_ci.yml/badge.svg)](https://github.com/OneInX/Manifest-InX/actions/workflows/manifestinx_ci.yml)
[![Release](https://img.shields.io/github/v/release/OneInX/Manifest-InX)](https://github.com/OneInX/Manifest-InX/releases)
[![License](https://img.shields.io/github/license/OneInX/Manifest-InX)](https://github.com/OneInX/Manifest-InX/blob/main/LICENSE)

## v2.0.0 — Core-only post-AI execution engine

Manifest-InX is a deterministic **post-AI execution engine** for contract-validated execution of structured outputs.

Core responsibilities:
- Deterministic canonicalization of inputs
- Contract validation (schema + invariants) with reproducible failures
- Auditability (hash-pinned artifacts and reproducible serialization)
- Pack System v0.1 (local-only): load and validate enterprise-owned packs

Example (pack-defined):
Depending on the pack, outputs may include deterministic intermediates such as stable identifiers or feature maps.
Core does not ship or assume any template catalog or vector taxonomy.

This repository **ships only the domain-agnostic engine core**.

### What does not ship in core
- No product apps/examples in the public install surface
- No bundled product templates/packs

## Usage

Recommended: call `validate_pack()` first to obtain a report; only load packs that validate cleanly.

```python
from manifestinx.engine import Engine

engine = Engine()

# Validate a local, hash-pinned pack (no network loading in v0.1)
report = engine.validate_pack("./path/to/pack")
if not report.ok:
    raise ValueError("Pack validation failed: " + "; ".join(i.message for i in report.issues))

# Load only after validation succeeds (recommended)
pack = engine.load_pack("./path/to/pack")
```

### Pack System v0.1 (local-only)

A pack is a local directory containing a `pack_manifest.json` that pins every file by `sha256`.
`validate_pack()` checks schema validity, path safety (no `..` / absolute paths), and sha256 pins computed over the referenced files’ **raw bytes** (no newline normalization or text transforms) for every listed file.

#### `pack_manifest.json` (v0.1)

Schema:
- Repo: `src/manifestinx/schemas/pack_manifest_v0_1.json`
- Installed (within site-packages): `manifestinx/schemas/pack_manifest_v0_1.json`

Required:
- `schema_version`: `"pack_manifest_v0.1"`
- `pack_id`: string
- `files`: map of `relpath -> sha256_hex` (raw bytes)

Optional (accepted for type/format only in v0.1):
- `version`: SemVer-like string
- `engine_compat`: `{ "min_version": "...", "max_version": "..." }`
- `entrypoints`: map of `name -> relpath` (relpath must be present in `files`)

## Install

```bash
python -m pip install manifestinx
```

## CLI

```bash
manifestinx --help
manifestinx pack validate ./path/to/pack
```
(Validates local packs only in v0.1; no network loading.)

## Determinism

- Determinism guarantee: identical inputs + the same validated pack (or no pack) produce identical canonicalization artifacts, validation decisions, and outputs defined by the pack-defined pipeline (including reproducible failures).
- Domain-specific behavior (templates, renderers, transforms, etc.) occurs only when a validated pack supplies pinned content and pack-provided entrypoints.

## Version

See `pyproject.toml` for the authoritative version.
