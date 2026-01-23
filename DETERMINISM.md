# Manifest-InX v2.x — Determinism Contract (Core Engine)

This document defines what “deterministic” means for the Manifest-InX v2.x **core-only** engine and Pack System v0.1.

## Scope

This contract applies to:

- Core engine fingerprint output for a given input text
- Pack validation decisions (schema + sha256 pins)
- Pack file reads via `PackHandle`

This contract does NOT define any domain semantics. Packs may attach domain meaning downstream.

## Deterministic Core Fingerprint

For a given input string `text`, the core engine produces a deterministic feature fingerprint:

- Input bytes: `text` encoded as UTF-8 bytes
- Digest: `sha256(input_bytes)`
- Output vector: a stable 5-dimensional distribution over dimension IDs:
  - `d01`, `d02`, `d03`, `d04`, `d05`
- Dominant dimension: the max-weight dimension ID (`dominant_dim`)

The stable fingerprint output consists of: `feature_dim_order`, `feature_vector`, `dominant_dim` (and optional `diagnostics`).

No meaning is implied by dimension IDs. They are stable identifiers; packs may interpret them.

### Determinism guarantee (core)

Given the same:
- `text` (exact same Unicode string)
Note: the core does not apply Unicode normalization; callers must provide identical strings to obtain identical fingerprints.
- core engine version (same `manifestinx` build)

The produced fingerprint (`d01..d05` + `dominant_dim`) is identical.

## Pack System v0.1 (Local Path Only)

v0.1 supports **local path** packs only.

A pack is a directory containing:

- `pack_manifest.json` at pack root
- The files referenced in the manifest

### Pack manifest validation

`validate_pack(pack_root)` is deterministic:

1) Schema validation of `pack_manifest.json` (Pack Manifest v0.1).
2) Safety checks on paths (relative only; no `..`; no absolute paths).
3) Hash-pin validation:
   - For each `relpath` in `files`, compute `sha256(raw_file_bytes)`
   - Compare against the pinned hex digest in the manifest

### Determinism guarantee (pack validation)

Given the same:
- pack directory contents (raw bytes)
- pack_manifest.json (raw bytes)
- manifest schema (v0.1)
- core engine version (same `manifestinx` build)

`validate_pack` produces the same `ValidationReport` (ok + issues) every time.

### Pack loading

`load_pack(pack_root)` requires `validate_pack` to pass, then returns a read-only `PackHandle`.
Reads via `PackHandle.read_bytes/read_text/read_json` are deterministic for the same on-disk bytes.

## No Network

Pack System v0.1 performs **no network** loading. All inputs are local filesystem paths.

