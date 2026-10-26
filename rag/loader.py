"""Load documents (Markdown, text, optional PDF) and split them into section-aware chunks."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

MAX_CHARS = 1200


@dataclass
class Chunk:
    id: str
    doc: str        # file name
    title: str      # document title
    section: str    # heading the chunk came from
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


def _front_matter(text: str) -> tuple[dict, str]:
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise ImportError("PDF support needs: pip install pypdf") from e
    return "\n\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


def _split_long(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split on paragraph boundaries, carrying the last paragraph over as overlap."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur = [], []
    for p in paras:
        if cur and sum(len(x) for x in cur) + len(p) > max_chars:
            out.append("\n\n".join(cur))
            cur = [cur[-1]] if len(cur[-1]) < max_chars // 3 else []
        cur.append(p)
    if cur:
        out.append("\n\n".join(cur))
    return out


def chunk_document(path: Path) -> list[Chunk]:
    raw = _read_pdf(path) if path.suffix.lower() == ".pdf" else path.read_text(encoding="utf-8")
    meta, body = _front_matter(raw)
    h1 = re.search(r"^# (.+)$", body, re.MULTILINE)
    title = meta.get("title") or (h1.group(1).strip() if h1 else path.stem)

    # split at level-2/3 headings so each chunk stays on one topic
    parts = re.split(r"^(#{2,3} .+)$", body, flags=re.MULTILINE)
    sections = [("Introduction", parts[0])]
    for i in range(1, len(parts), 2):
        sections.append((parts[i].lstrip("#").strip(), parts[i + 1] if i + 1 < len(parts) else ""))

    chunks = []
    for section, text in sections:
        text = re.sub(r"^# .+$", "", text, flags=re.MULTILINE).strip()
        if len(text) < 40:
            continue
        for j, piece in enumerate(_split_long(text)):
            cid = f"{path.stem}#{len(chunks)}"
            chunks.append(Chunk(cid, path.name, title, section if j == 0 else f"{section} (cont.)", piece))
    return chunks


def load_corpus(folder: Path | str) -> list[Chunk]:
    folder = Path(folder)
    files = sorted(p for p in folder.rglob("*") if p.suffix.lower() in {".md", ".txt", ".pdf"})
    if not files:
        raise FileNotFoundError(f"No .md/.txt/.pdf files found in {folder}")
    return [c for f in files for c in chunk_document(f)]
