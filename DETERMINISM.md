# Manifest-InX — Determinism

This document defines determinism guarantees for the **core engine**.

> Core determinism is about **reproducible transforms** and **provable artifacts**.
> It is not about forcing probabilistic models to behave deterministically.

---

## 1) Determinism boundary

Manifest-InX Core guarantees determinism for:

- Pack validation / gating (contract-first)
- Canonicalization of supported data types
- Stable serialization rules for proof targets
- Hashing rules that bind artifacts to:
  - input subsets
  - config subsets (explicit defaults)
  - pack references + pack sha256s
  - engine version

Core does NOT guarantee determinism for:

- any external provider generation (LLMs, diffusion, etc.)
- any network calls, timestamps, or environment-dependent behavior
- semantic identity of future “live” generations

---

## 2) Proof targets

A “proof target” is a canonical byte sequence that must be identical under the same deterministic conditions.

Core philosophy:
- Golden tests should assert **canonical artifact bytes** (and pinned hashes)
- Avoid “outer envelopes” that include volatile metadata (timestamps, debug info)

---

## 3) Deterministic identity

Core artifacts should support stable identity derivation without timestamps, typically from:
- canonicalized deterministic input subset
- deterministic config subset
- pack sha256s
- engine version

This enables:
- stable deduplication
- regression referencing
- long-lived reproducibility

---

## 4) How this relates to enterprise replay

Enterprises typically require:
- reproduce “what happened” exactly later
- audits, incident reviews, compliance checks
- governed change across model/policy upgrades

Those requirements are fulfilled by **Capture + Replay** at the SDK layer (not part of this repo), not by core alone.

See:
- `AI_INTEGRATION.md`
- `DETERMINISM_BOUNDARY.md`
