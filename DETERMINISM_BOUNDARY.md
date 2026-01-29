# Manifest-InX — Determinism Boundary

If you integrate probabilistic generators (LLMs), you must separate:

1) **Live Mode**: generation allowed, identical outputs are not promised
2) **Replay Mode**: no generation, byte-for-byte reproducibility is promised (requires capture)

---

## Live Mode (allowed, not promised identical)

Live Mode is useful for:
- interactive UX
- exploration / ideation
- “draft-first” workflows

In Live Mode, Manifest-InX Core can still guarantee:
- deterministic structure enforcement (schemas, gates)
- deterministic canonicalization
- deterministic proof target emission *for the engine-owned artifact*
but it cannot promise the provider will emit identical drafts in the future.

---

## Replay Mode (what enterprises buy)

Replay Mode means:
- no provider calls
- reproduce a previously captured episode exactly
- prove it via hashes + ordered audit events

Replay requires:
- a captured episode artifact
- pinned pack(s) + sha256s
- pinned deterministic config subset
- captured provider artifacts (or policy-approved deterministic summary)

Replay is primarily an **Enterprise SDK** responsibility.
Core supports the invariant foundations: canonicalization, hashing, pack pinning.
