"""Terminal chat.

    python cli.py "What does EMM cause 14 mean?"
    python cli.py                      # interactive
    python cli.py --sources-only "..."  # retrieval only, no API key needed
"""
from __future__ import annotations

import argparse
from pathlib import Path

from rag.answer import RAGAssistant
from rag.models import get_embedder, get_llm
from rag.retriever import HybridRetriever

KNOWLEDGE = Path(__file__).resolve().parent / "knowledge"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="?")
    p.add_argument("--sources-only", action="store_true", help="show retrieved passages without calling an LLM")
    p.add_argument("-k", type=int, default=4)
    args = p.parse_args()

    retriever = HybridRetriever.from_folder(KNOWLEDGE, embedder=None if args.sources_only else get_embedder())
    bot = None if args.sources_only else RAGAssistant(retriever, get_llm(), k=args.k)
    questions = [args.question] if args.question else iter(lambda: input("\nAsk (blank to quit): ").strip(), "")

    for q in questions:
        if bot is None:
            for i, h in enumerate(retriever.search(q, args.k), 1):
                print(f"\n[{i}] {h.chunk.title} > {h.chunk.section}  (bm25={h.bm25:.1f})\n{h.chunk.text[:400]}...")
            continue
        a = bot.ask(q)
        print(f"\n{a.text}\n")
        if not a.abstained:
            for s in a.sources:
                mark = "*" if s["n"] in a.cited else " "
                print(f" {mark}[{s['n']}] {s['title']} > {s['section']}")
            if not a.grounded:
                print("\n  Warning: answer is missing valid citations, so verify it before use.")


if __name__ == "__main__":
    main()
