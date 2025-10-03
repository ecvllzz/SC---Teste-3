# Supercadernos v5.0.0

Pipeline v5.0 (hardening) — CLI + cache JSON versionado + pré-filtro lexical + logging estruturado + persistência de intermediários e `resume`.
Este é um **esqueleto** pronto para receber a lógica de LLM. Os pontos de integração estão em `llm.py` e funções marcadas com `TODO`.

## Requisitos
- Python 3.11+
- Variável `GEMINI_API_KEY` (ou adapte `llm.py` para o provedor desejado)
- Dependências: ver `pyproject.toml`

## Estrutura
```
src/supercadernos/
  __init__.py
  __main__.py
  cli.py
  config.py
  cache.py
  llm.py
  pdfio.py
  indexer.py
  extractor.py
  consolidate.py
  synth.py
  report.py
  utils.py
prompts/
  extractor.jinja.md
  consolidator.jinja.md
  synopsis.jinja.md
config/
  stopwords.txt
artifacts/               # saídas geradas
```

## Uso rápido
```
# Instalar em modo desenvolvimento
pip install -e .

# Ver ajuda
supercadernos --help

# Simular (sem LLM): estima chamadas com pré-filtro
supercadernos run --dir ./entrada --dry-run

# Execução padrão (LLM precisa estar integrado em llm.py)
supercadernos run --dir ./entrada --out-sc supercaderno.md --out-sinopse sinopse.md

# Retomar após falha
supercadernos run --dir ./entrada --resume

# Modo econômico / determinístico
supercadernos run --dir ./entrada --economy
supercadernos run --dir ./entrada --deterministic
```
