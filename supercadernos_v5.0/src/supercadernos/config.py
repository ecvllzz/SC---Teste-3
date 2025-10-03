from __future__ import annotations
import os, yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .utils import ensure_dir

@dataclass
class ModelCfg:
    name: str
    temperature: float = 0.3
    safety: str = "default"  # default|relaxed|off

@dataclass
class LimitsCfg:
    max_workers_llm: int = 4
    min_hits_prefilter: int = 1
    window_pages: int = 1
    max_calls: Optional[int] = None

@dataclass
class PromptsCfg:
    extractor: str
    consolidator: str
    synopsis: str

@dataclass
class TextCfg:
    placeholder_vazio: str = "> ⚠️ Conteúdo não encontrado para este tópico."

@dataclass
class AppCfg:
    version: str = "5.0.0"
    artifacts_dir: str = "./artifacts"
    cache_dir: str = ".supercaderno_cache"

@dataclass
class Config:
    app: AppCfg
    models: Dict[str, ModelCfg]
    limits: LimitsCfg
    prompts: PromptsCfg
    text: TextCfg

def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    app = AppCfg(**raw.get("app", {}))
    models_raw = raw.get("models", {})
    models = {
        "flash": ModelCfg(**models_raw.get("flash", {})),
        "pro":   ModelCfg(**models_raw.get("pro",   {})),
    }
    limits = LimitsCfg(**raw.get("limits", {}))
    prompts = PromptsCfg(**raw.get("prompts", {}))
    text = TextCfg(**raw.get("text", {}))

    ensure_dir(app.artifacts_dir)
    ensure_dir(app.cache_dir)

    return Config(app=app, models=models, limits=limits, prompts=prompts, text=text)
