from __future__ import annotations
from typing import Optional

# Ponto único de integração LLM.
# v5.0: stubs seguros. Preencha com chamadas reais depois.
# Exemplo (quando integrar Gemini):
#   import google.generativeai as genai
#   genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_text_from_response(resp) -> str:
    """Normaliza respostas do SDK (placeholder)."""
    # TODO: implementar conforme provedor real
    return ""

def extract_topic_with_llm(topic: str, text_chunk: str, model_name: str, temperature: float, safety: str) -> str:
    # TODO: implementar chamada real
    return ""

def consolidate_with_llm(topic: str, snippets: list[str], model_name: str, temperature: float, safety: str) -> str:
    # TODO
    return ""

def synopsis_with_llm(topics: list[str], model_name: str, temperature: float, safety: str) -> str:
    # TODO
    return ""
