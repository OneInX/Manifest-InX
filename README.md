# Manifest-InX

[![CI](https://github.com/OneInX/Manifest-InX/actions/workflows/manifestinx_ci.yml/badge.svg)](https://github.com/OneInX/Manifest-InX/actions/workflows/manifestinx_ci.yml)
[![Release](https://img.shields.io/github/v/release/OneInX/Manifest-InX)](https://github.com/OneInX/Manifest-InX/releases)
[![License](https://img.shields.io/github/license/OneInX/Manifest-InX)](https://github.com/OneInX/Manifest-InX/blob/main/LICENSE)

## v2.0.1 — Core-only post-AI execution engine

Manifest-InX is a deterministic **post-AI execution engine** for contract-validated execution of structured outputs.

This repository **ships only the domain-agnostic engine core**.

### Core repository scope
- No product apps/examples in the public install surface
- No bundled product templates/packs
- No provider-specific integrations or “live LLM” wrappers

---

## Determinism (core vs live)

### Core Engine
Given **the same inputs** and **the same validated pack** (or no pack), the core engine provides reproducible, deterministic behavior for:

- Canonicalization artifacts (stable bytes / hashes for inputs)
- Contract validation (schema + invariants) with reproducible failures
- Pack validation decisions (schema + path safety + pinned hashes)
- Any pack-defined deterministic transforms that are **fully pinned** by the pack content

In other words: **determinism is guaranteed for pinned artifacts and deterministic transforms.**

### Live Provider Generation
If a workflow includes **live provider calls** (e.g., a model API), Manifest-InX does **not** guarantee output stability across time, model revisions, provider changes, sampling behavior, or infrastructure drift.

Enterprise-grade reproducibility is achieved via **capture → pin → replay**, not by assuming provider determinism.

---

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

---

## Pack System v0.1 (local-only)

A pack is a local directory containing a `pack_manifest.json` that pins every file by `sha256`.

`validate_pack()` checks:
- Schema validity
- Path safety (no `..` / absolute paths)
- sha256 pins computed over each referenced file’s **raw bytes**
  (no newline normalization or text transforms)

### `pack_manifest.json` (v0.1)

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

---

## Install

```bash
python -m pip install manifestinx
```

---

## CLI

```bash
manifestinx --help
manifestinx pack validate ./path/to/pack
```
(Validates local packs only in v0.1; no network loading.)

---

## Version

See `pyproject.toml` for the authoritative version.
