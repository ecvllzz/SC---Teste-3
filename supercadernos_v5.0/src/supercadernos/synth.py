from __future__ import annotations
from typing import List

def make_synopsis(topics_done: List[str]) -> str:
    """Gera uma sinopse simples (stub).
    A versão com LLM virá depois."""
    if not topics_done:
        return "- (sem tópicos)"
    bullets = [f"- {t}" for t in topics_done[:10]]
    return "\n".join(bullets)
