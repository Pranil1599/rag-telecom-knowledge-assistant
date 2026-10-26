import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
KNOWLEDGE = ROOT / "knowledge"


class FakeLLM:
    """Returns scripted replies and records the prompts it received (no API key needed)."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)

        class Msg:
            content = self.replies.pop(0)

        return Msg()


class FakeEmbedder:
    """Bag-of-letters embedding: crude, but enough to exercise the hybrid code path."""

    @staticmethod
    def _vec(text):
        text = text.lower()
        return [text.count(ch) for ch in "abcdefghijklmnopqrstuvwxyz0123456789"]

    def embed_documents(self, texts):
        return [self._vec(t) for t in texts]

    def embed_query(self, text):
        return self._vec(text)
