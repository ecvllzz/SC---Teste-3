from __future__ import annotations
from typing import List, Dict, Any
import os
from .utils import write_json, now_iso

def write_run_report(path: str, payload: dict) -> str:
    payload.setdefault("generated_at", now_iso())
    write_json(path, payload)
    return path
