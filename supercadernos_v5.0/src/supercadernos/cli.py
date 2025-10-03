from __future__ import annotations
import argparse, os, sys, json, time
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from .config import load_config
from .utils import ensure_dir, write_json, read_json, now_iso
from .indexer import discover_pdfs, choose_principal, build_run_inputs
from .pdfio import extract_text
from .extractor import prefilter, derive_keywords
from .consolidate import consolidate_snippets
from .synth import make_synopsis
from .report import write_run_report

console = Console()

def _dry_run_preview(pdfs: list[str], topics: list[str], min_hits: int) -> dict:
    stats = {"pairs": 0, "skipped": 0, "hits": 0, "by_doc": {}}
    for p in pdfs:
        text = extract_text(p).lower()
        by_topic = {}
        for t in topics:
            ok = prefilter(text, t, min_hits=min_hits)
            by_topic[t] = bool(ok)
            stats["pairs"] += 1
            if ok: stats["hits"] += 1
            else:  stats["skipped"] += 1
        stats["by_doc"][os.path.basename(p)] = by_topic
    return stats

def run_pipeline(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)

    # Diretórios
    ensure_dir(cfg.app.artifacts_dir)
    ensure_dir(cfg.app.cache_dir)

    # Descobrir PDFs e escolher principal
    pdfs = discover_pdfs(args.dir)
    if not pdfs:
        console.print("[red]Nenhum PDF encontrado em --dir[/red]"); return 2

    principal = choose_principal(pdfs, args.principal)
    if not principal:
        console.print("[yellow]Atenção:[/yellow] não foi possível determinar um 'roteiro principal'. Prosseguindo assim mesmo.")

    # Tópicos (v5.0 stub): substituir pela extração do roteiro principal na integração LLM
    topics = [
        "Introdução",
        "Teses centrais",
        "Jurisprudência relevante",
        "Pontos controversos",
        "Conclusões e próximos passos"
    ]

    # DRY-RUN: apenas estimação
    if args.dry_run:
        stats = _dry_run_preview(pdfs, topics, min_hits=(2 if args.economy else cfg.limits.min_hits_prefilter))
        table = Table(title="Prévia (dry-run) — pares doc×tópico")
        table.add_column("Documento")
        table.add_column("Tópicos com hit")
        for doc, by_topic in stats["by_doc"].items():
            hits = [t for t, ok in by_topic.items() if ok]
            table.add_row(doc, ", ".join(hits) if hits else "(nenhum)")
        console.print(table)
        console.print(f"[bold]Pairs:[/bold] {stats['pairs']}  [green]hits:[/green] {stats['hits']}  [yellow]skips:[/yellow] {stats['skipped']}")
        return 0

    # Execução (v5.0 sem LLM): persistir intermediários, consolidar com stub, sinopse stub
    inputs = build_run_inputs(pdfs)
    run_meta = {
        "app_version": cfg.app.version,
        "started_at": now_iso(),
        "inputs": inputs,
        "config_snapshot": {
            "models": {k: vars(v) for k, v in cfg.models.items()},
            "limits": vars(cfg.limits),
            "text": vars(cfg.text)
        },
        "flags": {
            "deterministic": bool(args.deterministic),
            "economy": bool(args.economy),
            "safety": args.safety
        }
    }

    # Pré-filtro por doc×tópico (sem LLM)
    min_hits = 2 if args.economy else cfg.limits.min_hits_prefilter
    coverage = {}
    for p in pdfs:
        text = extract_text(p).lower()
        hitlist = []
        for t in topics:
            if prefilter(text, t, min_hits=min_hits):
                hitlist.append(t)
        coverage[os.path.basename(p)] = hitlist

    # Intermediários
    inter_path = os.path.join(cfg.app.artifacts_dir, "conteudo_por_topico.json")
    conteudo_map = {t: [] for t in topics}

    # Stub: marcar apenas origem; integração LLM preencherá trechos reais
    for doc, hits in coverage.items():
        for t in hits:
            conteudo_map[t].append(f"(stub) Trecho relevante encontrado em {doc}.")

    write_json(inter_path, conteudo_map)

    # Consolidação (stub)
    sc_parts = []
    topics_done = []
    for t in topics:
        textos = conteudo_map.get(t, [])
        if not textos and args.strict:
            sc_parts.append(f"## {t}\n\n{cfg.text.placeholder_vazio}\n")
        elif not textos:
            sc_parts.append(f"## {t}\n\n")
        else:
            final = consolidate_snippets(textos)
            sc_parts.append(f"## {t}\n\n{final}\n")
            topics_done.append(t)

    sc_md = "\n".join(sc_parts)
    sc_path = os.path.join(cfg.app.artifacts_dir, args.out_sc)
    with open(sc_path, "w", encoding="utf-8") as f:
        f.write(sc_md)

    # Sinopse (stub)
    sinopse = make_synopsis(topics_done)
    sin_path = os.path.join(cfg.app.artifacts_dir, args.out_sinopse)
    with open(sin_path, "w", encoding="utf-8") as f:
        f.write(sinopse)

    # Resumo Markdown opcional no topo do SC
    if args.add_summary_header:
        summary = f"""<!-- resumo_gerado_automaticamente -->
**Resumo da execução**  
- Tópicos: {len(topics)}  
- Documentos: {len(pdfs)}  
- Tópicos com conteúdo: {len(topics_done)}  
- Data: {now_iso()}

---
"""
        with open(sc_path, "r", encoding="utf-8") as f:
            original = f.read()
        with open(sc_path, "w", encoding="utf-8") as f:
            f.write(summary + "\n" + original)

    # Relatório final
    run_meta.update({
        "ended_at": now_iso(),
        "outputs": {"supercaderno_md": sc_path, "sinopse_md": sin_path},
        "coverage": coverage,
        "topics_done": topics_done,
        "calls": {"flash_total": 0, "pro_total": 0, "cache_hits": 0, "cache_misses": 0}
    })
    report_path = os.path.join(cfg.app.artifacts_dir, "run_report.json")
    write_run_report(report_path, run_meta)

    console.print(f"[green]Supercaderno salvo em:[/green] {sc_path}")
    console.print(f"[green]Sinopse salva em:[/green] {sin_path}")
    console.print(f"[cyan]Relatório:[/cyan] {report_path}")
    return 0

def main():
    parser = argparse.ArgumentParser("supercadernos")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Executa o pipeline completo")
    run.add_argument("--dir", required=True)
    run.add_argument("--principal", required=False)
    run.add_argument("--config", default="config.yaml")
    run.add_argument("--out-sc", default="supercaderno.md")
    run.add_argument("--out-sinopse", default="sinopse.md")
    run.add_argument("--log-file", default=None)
    run.add_argument("--log-level", default="INFO")
    run.add_argument("--deterministic", action="store_true")
    run.add_argument("--safety", choices=["default","relaxed","off"], default="default")
    run.add_argument("--economy", action="store_true")
    run.add_argument("--max-calls", type=int, default=None)
    run.add_argument("--max-workers-llm", type=int, default=None)
    run.add_argument("--strict", action="store_true")
    run.add_argument("--add-summary-header", action="store_true")
    run.add_argument("--resume", action="store_true")
    run.add_argument("--dry-run", action="store_true")
    run.set_defaults(func=run_pipeline)

    args = parser.parse_args()
    code = args.func(args)
    raise SystemExit(code)
