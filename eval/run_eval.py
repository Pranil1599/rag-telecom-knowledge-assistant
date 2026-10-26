"""Evaluate the assistant.

    python eval/run_eval.py                 # retrieval only (offline, no API key): Hit@1, Hit@k, MRR
    python eval/run_eval.py --answers       # also generate answers with the LLM and check
                                            # groundedness (valid citations) and keyword coverage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag.retriever import HybridRetriever  # noqa: E402


def retrieval_eval(retriever: HybridRetriever, cases: list[dict], k: int = 4) -> dict:
    hit1 = hitk = rr = 0.0
    rows = []
    for c in cases:
        docs = [h.chunk.doc for h in retriever.search(c["question"], k)]
        # a case can list several docs that legitimately contain the answer
        ranks = [i + 1 for i, d in enumerate(docs) if d in c["expected_docs"]]
        rank = ranks[0] if ranks else None
        hit1 += rank == 1
        hitk += rank is not None
        rr += 1 / rank if rank else 0
        rows.append({"question": c["question"], "rank": rank, "top_docs": docs})
    n = len(cases)
    return {"hit@1": hit1 / n, f"hit@{k}": hitk / n, "mrr": rr / n, "rows": rows}


def answer_eval(retriever: HybridRetriever, cases: list[dict], model: str | None) -> dict:
    from rag.answer import RAGAssistant
    from rag.models import get_llm

    bot = RAGAssistant(retriever, get_llm(model))
    grounded = covered = 0
    rows = []
    for c in cases:
        a = bot.ask(c["question"])
        kw_ok = all(k.lower() in a.text.lower() for k in c.get("keywords", []))
        grounded += a.grounded
        covered += kw_ok
        rows.append({"question": c["question"], "grounded": a.grounded, "keywords_ok": kw_ok, "answer": a.text})
    n = len(cases)
    return {"grounded_rate": grounded / n, "keyword_coverage": covered / n, "rows": rows}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--answers", action="store_true")
    p.add_argument("--model")
    p.add_argument("-k", type=int, default=4)
    args = p.parse_args()

    cases = json.loads((ROOT / "eval" / "questions.json").read_text())
    from rag.models import get_embedder

    retriever = HybridRetriever.from_folder(ROOT / "knowledge", embedder=get_embedder())
    report = {"retrieval": retrieval_eval(retriever, cases, args.k)}
    r = report["retrieval"]
    print(f"Retrieval  Hit@1 {r['hit@1']:.0%}  Hit@{args.k} {r[f'hit@{args.k}']:.0%}  MRR {r['mrr']:.2f}  ({len(cases)} questions)")
    for row in r["rows"]:
        if row["rank"] != 1:
            print(f"  rank={row['rank']}  {row['question']}")

    if args.answers:
        report["answers"] = answer_eval(retriever, cases, args.model)
        a = report["answers"]
        print(f"Answers    grounded {a['grounded_rate']:.0%}  keyword coverage {a['keyword_coverage']:.0%}")

    (ROOT / "eval" / "results.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
