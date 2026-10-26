"""Small, dependency-free BM25 keyword retriever tuned for telecom text.

Telecom questions are full of exact identifiers (IR.21, S6a, 5004, EMM #14) that embeddings
often blur, so keyword search is kept as a first-class signal next to dense retrieval.
"""
from __future__ import annotations

import math
import re
from collections import Counter

STOPWORDS = set("""a an and are as at be by can do does for from has have how i if in is it its of on or
that the this to was what when where which who why will with you your""".split())


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = []
    for tok in re.findall(r"[a-z0-9]+(?:[.\-/][a-z0-9]+)*", text):
        if tok in STOPWORDS:
            continue
        tokens.append(tok)
        if re.search(r"[.\-/]", tok):  # 'ir.21' -> also 'ir', '21'; 'epc.mnc001' -> parts
            tokens.extend(p for p in re.split(r"[.\-/]", tok) if p and p not in STOPWORDS)
    return tokens


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tfs = [Counter(tokenize(d)) for d in docs]
        self.lens = [sum(tf.values()) for tf in self.tfs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(t for tf in self.tfs for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for tf, length in zip(self.tfs, self.lens):
            s = 0.0
            for t in q:
                f = tf.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out
