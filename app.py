"""Streamlit chat UI:  streamlit run app.py"""
from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from rag.answer import RAGAssistant
from rag.loader import load_corpus
from rag.models import get_embedder, get_llm
from rag.retriever import HybridRetriever

KNOWLEDGE = Path(__file__).resolve().parent / "knowledge"

st.set_page_config(page_title="Telecom Roaming Knowledge Assistant", layout="wide")
st.title("Telecom Roaming Knowledge Assistant")
st.caption("RAG over IREG / roaming notes. Every answer cites its sources; the assistant says so when the answer is not in the documents.")


@st.cache_resource
def build(extra_files: tuple[str, ...] = ()) -> RAGAssistant:
    chunks = load_corpus(KNOWLEDGE)
    if extra_files:
        chunks += load_corpus(Path(extra_files[0]).parent)
    return RAGAssistant(HybridRetriever(chunks, embedder=get_embedder()), get_llm())


with st.sidebar:
    st.subheader("Add your own documents")
    uploads = st.file_uploader("PDF, Markdown or text (e.g. 3GPP specs, your IR.21 notes)",
                               type=["pdf", "md", "txt"], accept_multiple_files=True)
    extra: tuple[str, ...] = ()
    if uploads:
        tmp = Path(tempfile.mkdtemp())
        for f in uploads:
            (tmp / f.name).write_bytes(f.getvalue())
        extra = tuple(str(tmp / f.name) for f in uploads)
    st.markdown("**Try:**\n- What does EMM cause 14 mean?\n- ULA returned 5004, what now?\n"
                "- Both CS and PS attach fail on a test SIM\n- What is S8HR?")

bot = build(extra)
st.session_state.setdefault("history", [])

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

if question := st.chat_input("Ask a roaming / IREG question"):
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            ans = bot.ask(question)
        st.markdown(ans.text)
        if not ans.abstained:
            if not ans.grounded:
                st.warning("This answer is missing valid citations. Verify it before using it.")
            with st.expander("Sources"):
                for s, h in zip(ans.sources, ans.hits):
                    star = "**(cited)**" if s["n"] in ans.cited else ""
                    st.markdown(f"**[{s['n']}] {s['title']} > {s['section']}** {star}")
                    st.caption(h.chunk.text[:500] + ("..." if len(h.chunk.text) > 500 else ""))
    st.session_state.history.append({"role": "assistant", "content": ans.text})
