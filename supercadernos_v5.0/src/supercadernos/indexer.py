from __future__ import annotations
from typing import List, Dict, Any
import os
from .utils import read_json, write_json, file_sha256
from .pdfio import extract_text
from .config import Config

def discover_pdfs(input_dir: str) -> list[str]:
    pdfs = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return sorted(pdfs)

def choose_principal(pdfs: list[str], hinted: str | None) -> str | None:
    if hinted:
        for p in pdfs:
            if os.path.basename(p) == hinted:
                return p
    for p in pdfs:
        name = os.path.basename(p).lower()
        if "roteiro" in name or "principal" in name:
            return p
    return max(pdfs, key=lambda x: os.path.getsize(x)) if pdfs else None

def build_run_inputs(pdfs: list[str]) -> list[dict]:
    items = []
    for p in pdfs:
        try:
            pages = None
            try:
                import fitz
                with fitz.open(p) as doc:
                    pages = len(doc)
            except Exception:
                pages = None
            items.append({
                "path": p,
                "name": os.path.basename(p),
                "size_bytes": os.path.getsize(p),
                "sha256": file_sha256(p),
                "pages": pages
            })
        except Exception:
            items.append({"path": p, "name": os.path.basename(p)})
    return items
