# Manifest-InX — AI Integration

Manifest-InX is designed to sit *around* probabilistic generation and make the overall system auditable and reproducible.

---

## Recommended flow (draft → gate → canonical artifact)

1) **Draft generation (optional)**
   - Call an LLM (or any provider) to produce a draft.
   - Accept that it can vary across runs.

2) **Gate + normalize (core)**
   - Validate against explicit contracts (pack-defined schemas).
   - Canonicalize and enforce invariants.
   - Produce deterministic proof target bytes.

3) **Emit the engine-owned artifact**
   - The canonical artifact (episode, plan, storyboard, etc.) is what the engine proves.
   - This artifact is what you golden-test.

---

## Capture + Replay (enterprise posture)

If you need reproducibility of a specific “decision-grade” run:
- Capture the run as an **Episode**
- Store minimal artifacts required by policy
- Replay later with no provider calls

Capture/Replay is policy-driven:
- capture only high-risk / regulated / customer-impacting runs
- apply redaction boundaries
- apply retention schedules
- bring-your-own storage (S3/GCS/Azure/on-prem)

This posture is implemented by the Enterprise SDK (not part of this repo).
Core remains a public, stable foundation.
