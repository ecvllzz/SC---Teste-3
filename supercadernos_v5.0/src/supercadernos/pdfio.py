from __future__ import annotations
from typing import Optional
import os

def extract_text(path: str) -> str:
    """Extrai texto de um PDF. Tenta PyMuPDF; se indisponível, usa pypdf.
    Retorna sempre string (pode ser vazia)."""
    text = ""
    try:
        import fitz  # PyMuPDF
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text("text")
        return text or ""
    except Exception:
        pass

    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text or ""
    except Exception:
        return ""
