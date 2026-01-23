# Manifest-InX v2.x — API Stability (Core Engine)

This repository is the **core-only**, **domain-agnostic** Manifest-InX engine with Pack System v0.1.
It is the foundation for enterprise SDK work, but it is not itself the enterprise SDK.

## Supported Public Surface (v2.x)

Only the following interfaces are considered **stable** within the v2.x major line.

### Python (stable)

- `manifestinx.Engine`
  - `Engine.run_text(text: str, *, diagnostics: bool = False) -> dict[str, Any]`
    - Output dictionary (stable top-level keys in v2.x):
        - `feature_dim_order`: array of dimension ids, fixed as `["d01","d02","d03","d04","d05"]`
        - `feature_vector`: array of 5 floats aligned with `feature_dim_order`
        - `dominant_dim`: one of `d01..d05`
        - if `diagnostics=True`: includes `diagnostics` (object). Contents may evolve within v2.x.
  - `Engine.validate_pack(path: str | pathlib.Path) -> ValidationReport`
  - `Engine.load_pack(path: str | pathlib.Path) -> PackHandle`

- `manifestinx.pack_system`
  - `validate_pack(pack_root: str | pathlib.Path) -> ValidationReport`
  - `load_pack(pack_root: str | pathlib.Path) -> PackHandle`

- Types (stable)
  - `ValidationReport`
  - `ValidationIssue`
  - `PackHandle`

### CLI (stable)

- `manifestinx pack validate <path> [--json]`

## Everything Else Is Internal

Only the keys listed above are stable; additional keys may be added, but existing stable keys will not be removed or renamed within v2.x.

Any other modules, functions, fields, or file layouts not listed above are **internal** and may change at any time
(including in minor/patch releases) without notice.

## Versioning Policy

- v2.x: backward compatible for the supported public surface above.
- v3.0.0+: breaking changes may occur (with release notes).

