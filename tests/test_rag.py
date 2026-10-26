import json
import tempfile
from pathlib import Path

from conftest import KNOWLEDGE, ROOT, FakeEmbedder, FakeLLM

from rag.answer import NOT_FOUND, RAGAssistant, check_citations
from rag.bm25 import tokenize
from rag.loader import chunk_document, load_corpus
from rag.retriever import HybridRetriever

RETRIEVER = HybridRetriever.from_folder(KNOWLEDGE)


def test_tokenizer_keeps_telecom_identifiers():
    toks = tokenize("Check IR.21 and S6a, EMM cause #14, epc.mnc001.mcc643")
    assert {"ir.21", "ir", "21", "s6a", "14", "epc.mnc001.mcc643", "mnc001"} <= set(toks)


def test_chunks_are_section_aware():
    chunks = chunk_document(KNOWLEDGE / "04-diameter-s6a-result-codes.md")
    assert chunks[0].title == "Diameter S6a Result Codes for LTE Roaming"
    assert any(c.section == "Troubleshooting hints" for c in chunks)
    assert all(c.text.strip() for c in chunks)


def test_loader_reads_txt_and_splits_long_text():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "notes.txt").write_text("\n\n".join(f"Paragraph {i} about roaming. " * 20 for i in range(10)))
    chunks = load_corpus(tmp)
    assert len(chunks) > 1 and all(len(c.text) <= 1300 for c in chunks)


def test_retrieval_finds_expected_docs():
    cases = json.loads((ROOT / "eval" / "questions.json").read_text())
    for c in cases:
        top = [h.chunk.doc for h in RETRIEVER.search(c["question"], 4)]
        assert set(top) & set(c["expected_docs"]), c["question"]


def test_hybrid_mode_runs_with_embeddings():
    r = HybridRetriever.from_folder(KNOWLEDGE, embedder=FakeEmbedder())
    hits = r.search("Diameter 5004 roaming not allowed", 3)
    assert len(hits) == 3 and hits[0].score > 0


def test_citation_check():
    assert check_citations("A [1]. B [2][3]. C [7].", 4) == ([1, 2, 3], [7])


def test_answer_is_grounded_and_cites():
    llm = FakeLLM("EMM cause #14 means EPS services are not allowed in this PLMN [1].")
    a = RAGAssistant(RETRIEVER, llm).ask("What does EMM cause 14 mean?")
    assert a.grounded and a.cited == [1] and not a.abstained
    prompt = llm.calls[0][1][1]
    assert "[1]" in prompt and "EPS services not allowed in this PLMN" in prompt


def test_uncited_or_invalid_answer_is_flagged():
    a = RAGAssistant(RETRIEVER, FakeLLM("Cause 14 is bad.")).ask("What does EMM cause 14 mean?")
    assert not a.grounded
    a = RAGAssistant(RETRIEVER, FakeLLM("See [9].")).ask("What does EMM cause 14 mean?")
    assert not a.grounded and a.invalid_citations == [9]


def test_abstains_on_out_of_scope_question_without_calling_llm():
    llm = FakeLLM()  # no replies: any LLM call would fail
    a = RAGAssistant(RETRIEVER, llm).ask("Recommend a good pasta recipe")
    assert a.abstained and a.text == NOT_FOUND and llm.calls == []


def test_model_not_found_reply_becomes_abstention():
    a = RAGAssistant(RETRIEVER, FakeLLM(NOT_FOUND)).ask("What is the IREG test window for partner X?")
    assert a.abstained


def test_index_save_and_load_roundtrip():
    path = Path(tempfile.mkdtemp()) / "index.json"
    RETRIEVER.save(path)
    loaded = HybridRetriever.load(path)
    assert len(loaded.chunks) == len(RETRIEVER.chunks)
    assert loaded.search("TADIG code", 1)[0].chunk.doc == RETRIEVER.search("TADIG code", 1)[0].chunk.doc
