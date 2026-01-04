import json, hashlib, pathlib

m = json.loads(pathlib.Path(r"src/microinx/data/microinx_manifest_v1.json").read_text(encoding="utf-8"))
manifest = m["files"]["engine.py"] if "files" in m else m["engine.py"]

b = pathlib.Path(r"src/microinx/engine.py").read_bytes()
print("manifest:", manifest)
print("sha(raw):", hashlib.sha256(b).hexdigest())
print("sha(lf): ", hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest())
