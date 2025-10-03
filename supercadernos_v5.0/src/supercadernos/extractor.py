from __future__ import annotations
from typing import List, Dict, Any, Tuple
import re
from unidecode import unidecode
from .utils import normalize_text
from .config import Config

def derive_keywords(topic: str) -> list[str]:
    # Simples: tokeniza, remove símbolos, minúsculas, sem acento
    base = re.findall(r"[\wáéíóúâêîôûãõç]+", topic, flags=re.IGNORECASE)
    kws = [unidecode(t.lower()) for t in base if len(t) > 2]
    return list(dict.fromkeys(kws))  # dedupe preservando ordem

def prefilter(doc_text: str, topic: str, min_hits: int = 1) -> bool:
    corpus = unidecode(doc_text.lower())
    hits = sum(1 for kw in derive_keywords(topic) if kw in corpus)
    return hits >= min_hits
