from __future__ import annotations
from typing import List

def consolidate_snippets(snippets: List[str]) -> str:
    """Consolida trechos em um parágrafo curto.
    v5.0 mantém stub simples; a versão com LLM entra depois."""
    clean = [s.strip() for s in snippets if s and s.strip()]
    if not clean:
        return ""
    return "\n".join(clean[:5])
