"""Hybrid retriever: BM25 keywords + optional dense embeddings, fused with Reciprocal Rank Fusion."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from .bm25 import BM25
from .loader import Chunk, load_corpus

INDEX_PATH = Path(__file__).resolve().parent.parent / ".index" / "index.json"


@dataclass
class Hit:
    chunk: Chunk
    score: float        # fused RRF score
    bm25: float         # raw keyword score (used for the "is this answerable?" check)


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def _ranks(scores: list[float]) -> dict[int, int]:
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return {i: r for r, i in enumerate(order) if scores[i] > 0}


class HybridRetriever:
    def __init__(self, chunks: list[Chunk], embedder=None, vectors: list[list[float]] | None = None, rrf_k: int = 60):
        self.chunks = chunks
        self.bm25 = BM25([f"{c.title}\n{c.section}\n{c.text}" for c in chunks])
        self.embedder = embedder
        self.vectors = vectors
        if embedder is not None and vectors is None:
            self.vectors = embedder.embed_documents([f"{c.section}\n{c.text}" for c in chunks])
        self.rrf_k = rrf_k

    @classmethod
    def from_folder(cls, folder, embedder=None) -> "HybridRetriever":
        return cls(load_corpus(folder), embedder=embedder)

    def search(self, query: str, k: int = 4) -> list[Hit]:
        kw = self.bm25.scores(query)
        rankings = [_ranks(kw)]
        if self.embedder is not None and self.vectors:
            qv = self.embedder.embed_query(query)
            rankings.append(_ranks([_cosine(qv, v) for v in self.vectors]))
        fused: dict[int, float] = {}
        for ranking in rankings:
            for i, r in ranking.items():
                fused[i] = fused.get(i, 0.0) + 1.0 / (self.rrf_k + r + 1)
        top = sorted(fused, key=fused.get, reverse=True)[:k]
        return [Hit(self.chunks[i], fused[i], kw[i]) for i in top]

    # ---- persistence (so embeddings are computed once) -----------------
    def save(self, path: Path = INDEX_PATH) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"chunks": [c.to_dict() for c in self.chunks], "vectors": self.vectors}))
        return path

    @classmethod
    def load(cls, path: Path = INDEX_PATH, embedder=None) -> "HybridRetriever":
        data = json.loads(Path(path).read_text())
        vectors = data.get("vectors") if embedder is not None else None
        return cls([Chunk(**c) for c in data["chunks"]], embedder=embedder, vectors=vectors)
