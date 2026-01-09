# ADAPTER_QUICKSTART.md

## Run locally

```bash
python -m manifestinx.api --host 127.0.0.1 --port 8080
```

## Smoke test

```bash
curl -s http://127.0.0.1:8080/health
```

```bash
curl -s -X POST http://127.0.0.1:8080/insight \
  -H "Content-Type: application/json" \
  -d '{"text":"I overthink decisions and delay action."}'
```

Notes:
- This stays engine-layer (adapter) and does not replace the pack-branded demo entrypoint (`inxzap-demo`).
