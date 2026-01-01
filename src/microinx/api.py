# api.py
# MicroInX — Integration Adapter v1.0 (Sprint 4)
# Minimal local JSON API wrapper. No engine logic changes.

from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

try:
    # Python 3.7+
    from http.server import ThreadingHTTPServer as _HTTPServer
except Exception:  # pragma: no cover
    from http.server import HTTPServer as _HTTPServer

# Existing deterministic entrypoint (Release Candidate Pack)
import microinx.run as run


MANIFEST_PATH = os.environ.get("MICROINX_MANIFEST_PATH", "microinx_manifest_v1.json")


def _read_manifest_version(path: str = MANIFEST_PATH) -> str:
    with open(path, "r", encoding="utf-8") as f:
        m = json.load(f)
    v = m.get("version")
    if not isinstance(v, str) or not v:
        raise RuntimeError("manifest missing version")
    return v


def verify_release_or_raise() -> str:
    """Verifies release integrity before serving.

    Returns:
      version string from manifest, if verification passes.

    Raises:
      RuntimeError if any manifest hash mismatch occurs.
    """
    run.verify_release()
    return _read_manifest_version()


class MicroInXAPIHandler(BaseHTTPRequestHandler):
    server_version = "MicroInXAPI/1.0"
    protocol_version = "HTTP/1.1"

    # injected at server construction
    _release_version: str = "1.0.0"

    def log_message(self, format: str, *args) -> None:  # pragma: no cover
        # keep quiet for deterministic test output
        return

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return

        self._send_json(
            HTTPStatus.OK,
            {"status": "ok", "version": self._release_version},
        )

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/insight":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return

        try:
            n = int(self.headers.get("Content-Length", "0"))
        except Exception:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "bad_content_length"})
            return

        raw = self.rfile.read(n)
        try:
            req = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "bad_json"})
            return

        text = req.get("text") if isinstance(req, dict) else None
        if not isinstance(text, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "missing_text"})
            return

        try:
            r = run.run(text)
        except Exception as e:
            # minimal error surface; do not add new semantics
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "engine_error", "detail": str(e)})
            return

        out = {
            "template_id": r.get("template_id"),
            "output_text": r.get("output_text"),
            "sdt": r.get("sdt"),
            "manifest": {"version": self._release_version, "hash_ok": True},
        }
        self._send_json(HTTPStatus.OK, out)


def make_server(host: str = "127.0.0.1", port: int = 8080) -> _HTTPServer:
    version = verify_release_or_raise()

    class _H(MicroInXAPIHandler):
        _release_version = version

    return _HTTPServer((host, port), _H)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="api")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args(argv)

    # Refuse to serve if release integrity fails.
    httpd = make_server(args.host, args.port)

    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())