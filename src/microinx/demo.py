# demo.py
# MicroInX — One-Command Demo Pack v1.0 (Sprint 6)
# Wrapper only: verifies release, starts local API server, sends one demo request, prints response, exits.
# No engine/mapping/SDT/template/manifest/contract changes.

from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.request
from typing import Any, Dict

import microinx.api as api
import microinx.run as run


HOST_DEFAULT = "127.0.0.1"
PORT_DEFAULT = 8080  # fixed default demo port (matches the v1.0 OpenAPI server URL)

# Optional overrides (do not change defaults):
# - MICROINX_DEMO_HOST
# - MICROINX_DEMO_PORT

DEMO_INPUT_TEXT = "Need more context and more research; later it depends. I revisit again and still."


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        return json.loads(r.read().decode("utf-8"))


def verify_release() -> str:
    """Verify release integrity (manifest hashes) and return release version."""
    # Strong gate (refuses on any hash mismatch).
    run.verify_release()
    # Stable version string from manifest.
    return api.verify_release_or_raise()


def run_demo(host: str = HOST_DEFAULT, port: int = PORT_DEFAULT) -> Dict[str, Any]:
    """Run the one-command demo and return the response JSON.

    Default port is fixed (8080). Tests may pass port=0 to avoid conflicts.
    """
    # Explicit preflight: verify manifest before starting server.
    _ = verify_release()

    httpd = api.make_server(host, port)
    srv_host, srv_port = httpd.server_address
    base = f"http://{srv_host}:{srv_port}"

    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    try:
        time.sleep(0.05)  # minimal startup settle
        resp = _post_json(base + "/insight", {"text": DEMO_INPUT_TEXT})
        return resp
    finally:
        httpd.shutdown()
        httpd.server_close()


def _env_port(default: int) -> int:
    s = os.getenv("MICROINX_DEMO_PORT")
    if not s:
        return default
    try:
        p = int(s)
    except ValueError as e:
        raise ValueError(f"MICROINX_DEMO_PORT must be an int, got: {s!r}") from e
    return p


def main() -> int:
    host = os.getenv("MICROINX_DEMO_HOST", HOST_DEFAULT)

    try:
        port = _env_port(PORT_DEFAULT)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    try:
        r = run_demo(host=host, port=port)
    except OSError as e:
        # Cross-platform "port in use" errno values:
        # Linux: 98, macOS: 48, Windows: 10048
        if getattr(e, "errno", None) in (98, 48, 10048):
            print(
                f"ERROR: port {port} is already in use. "
                f"Either free it, or set MICROINX_DEMO_PORT to an available port and rerun.",
                file=sys.stderr,
            )
            return 2
        raise

    print(json.dumps(r, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())