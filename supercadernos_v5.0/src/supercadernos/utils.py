from __future__ import annotations
import os, re, json, hashlib, unicodedata, pathlib, time
from typing import Iterable, List, Dict, Any
from unidecode import unidecode

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def slugify(s: str) -> str:
    s = unidecode(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "n-a"

def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(s: str) -> str:
    # Normaliza acentos e espaços
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def now_iso() -> str:
    import datetime
    return datetime.datetime.now().isoformat(timespec="seconds")
