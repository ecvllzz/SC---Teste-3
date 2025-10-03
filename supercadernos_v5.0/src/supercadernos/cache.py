from __future__ import annotations
import os, json, time, hashlib
from typing import Optional, Tuple
from .utils import ensure_dir, sha256_str

def _key(model: str, temp: float, safety: str, prompt_hash: str, app_version: str) -> str:
    base = f"{model}|{temp}|{safety}|{prompt_hash}|v{app_version}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def get(cache_dir: str, key: str) -> Optional[dict]:
    path = os.path.join(cache_dir, f"{key}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def set(cache_dir: str, key: str, text: str, meta: dict) -> str:
    ensure_dir(cache_dir)
    path = os.path.join(cache_dir, f"{key}.json")
    payload = {"text": text, "meta": meta}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path

def make_key(model: str, temp: float, safety: str, prompt_text: str, app_version: str) -> str:
    prompt_hash = sha256_str(prompt_text)
    return _key(model, temp, safety, prompt_hash, app_version)
