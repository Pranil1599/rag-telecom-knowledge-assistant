"""Model factories. Configure with env vars (or a .env file):

    LLM_MODEL=openai:gpt-4o-mini | anthropic:claude-sonnet-4-5 | ollama:llama3.1
    EMBED_MODEL=openai:text-embedding-3-small   (optional; leave empty for keyword-only retrieval)
"""
from __future__ import annotations

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_llm(model: str | None = None):
    from langchain.chat_models import init_chat_model

    return init_chat_model(model or os.getenv("LLM_MODEL", "openai:gpt-4o-mini"), temperature=0)


def get_embedder(model: str | None = None):
    model = model or os.getenv("EMBED_MODEL", "")
    if not model:
        return None
    from langchain.embeddings import init_embeddings

    return init_embeddings(model)
