"""Grounded answering: numbered context, mandatory [n] citations, abstain when retrieval is weak."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .retriever import Hit, HybridRetriever

SYSTEM = """You are a telecom roaming expert helping an IREG / roaming operations analyst.
Answer ONLY from the numbered context passages. Rules:
- Cite every factual sentence with the passage number in square brackets, e.g. [1] or [2][3].
- If the context does not contain the answer, reply exactly: "I could not find this in the knowledge base."
- Be concise and practical: short paragraphs or bullet points, include cause values / codes when relevant.
- Never invent spec numbers, cause codes or procedures that are not in the context."""

NOT_FOUND = "I could not find this in the knowledge base."


@dataclass
class Answer:
    question: str
    text: str
    hits: list[Hit]
    cited: list[int] = field(default_factory=list)       # passage numbers the model cited
    invalid_citations: list[int] = field(default_factory=list)
    grounded: bool = True                                 # False if the answer has no valid citation
    abstained: bool = False

    @property
    def sources(self) -> list[dict]:
        return [{"n": i + 1, "doc": h.chunk.doc, "title": h.chunk.title, "section": h.chunk.section}
                for i, h in enumerate(self.hits)]


def format_context(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{i + 1}] ({h.chunk.title} > {h.chunk.section})\n{h.chunk.text}" for i, h in enumerate(hits))


def check_citations(text: str, n_passages: int) -> tuple[list[int], list[int]]:
    nums = sorted({int(n) for n in re.findall(r"\[(\d+)\]", text)})
    return [n for n in nums if 1 <= n <= n_passages], [n for n in nums if not 1 <= n <= n_passages]


class RAGAssistant:
    def __init__(self, retriever: HybridRetriever, llm, k: int = 4, min_bm25: float = 1.5):
        self.retriever, self.llm, self.k, self.min_bm25 = retriever, llm, k, min_bm25

    def ask(self, question: str) -> Answer:
        hits = self.retriever.search(question, self.k)
        # Abstain without calling the LLM when nothing relevant was retrieved.
        weak = max((h.bm25 for h in hits), default=0.0) < self.min_bm25
        if not hits or (weak and self.retriever.embedder is None):
            return Answer(question, NOT_FOUND, hits, grounded=False, abstained=True)

        reply = self.llm.invoke([("system", SYSTEM),
                                 ("human", f"Context:\n{format_context(hits)}\n\nQuestion: {question}")])
        text = getattr(reply, "content", reply)
        if isinstance(text, list):
            text = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in text)
        text = str(text).strip()

        if NOT_FOUND.lower() in text.lower():
            return Answer(question, NOT_FOUND, hits, grounded=False, abstained=True)
        cited, invalid = check_citations(text, len(hits))
        return Answer(question, text, hits, cited, invalid, grounded=bool(cited) and not invalid)
