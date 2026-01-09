# Manifest-InX API Contract (v1.0)

This document freezes the external contract for the Manifest-InX Integration Adapter v1.0.

## Endpoints

### GET /health

Response (200):

- `status` (string) — always `"ok"`
- `version` (string) — release version from the Manifest-InX manifest

### POST /insight

Request body:

- `text` (string, required)

Response (200):

- `template_id` (string)
- `output_text` (string)
- `sdt` (object)
  - `pass` (boolean)
  - `violations` (string[])
- `manifest` (object)
  - `version` (string)
  - `hash_ok` (boolean)

## Error shapes

All errors are JSON objects with:

- `error` (string)
- `detail` (string, optional)

Observed error codes in v1.0:

- 400: `bad_json` | `missing_text` | `bad_content_length`
- 404: `not_found`
- 500: `engine_error` (with `detail`)

## Determinism

For identical request bodies to `POST /insight`, the server must return identical values for:

- `template_id`
- `output_text`
- `sdt`

No RNG, no time-based behavior, and no external calls are permitted in the v1.0 contract surface.

## Versioning rule

- Contract file: `openapi_manifestinx_v1.yaml` is format-stable for v1.x.
- Release version is returned via `/health.version` and `manifest.version`.

## Release integrity (server refusal)

Before serving, the adapter verifies the release manifest hashes.
If a required file hash mismatches, the server refuses to start (no HTTP response).
