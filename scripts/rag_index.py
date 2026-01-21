from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    source_path: str


def log(msg: str) -> None:
    print(f"[rag_index] {msg}", flush=True)


def safe_read_text(path: Path) -> str:
    """
    Windows potrafi mieć pliki zapisane różnymi encodingami.
    Próbujemy UTF-8, a jak nie zadziała, to fallback.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        log(f"WARNING: utf-8 decode failed for {path.name}, trying cp1250")
        return path.read_text(encoding="cp1250", errors="replace")
    except Exception as e:
        log(f"ERROR: could not read {path}: {e}")
        return ""


def safe_chunk(text: object, max_chars: int = 800) -> List[str]:
    # FIX: odporność na None / inne typy
    if not isinstance(text, str):
        return []

    text = text.strip()
    if not text:
        return []

    chunks: List[str] = []
    for i in range(0, len(text), max_chars):
        ch = text[i : i + max_chars].strip()
        if ch:
            chunks.append(ch)
    return chunks


def main() -> None:
    t_start = time.time()

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
    collection_name = os.getenv("CHROMA_COLLECTION", "bess_public")
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    log("Starting indexing")
    log(f"Base dir: {base_dir}")
    log(f"Data dir: {data_dir}")
    log(f"Chroma dir: {persist_dir}")
    log(f"Collection: {collection_name}")
    log(f"Embedding model: {model_name}")

    # 1) Load embedding model
    log("Loading embedding model (this can take a while on first run)...")
    embedder = SentenceTransformer(model_name)
    log("Embedding model loaded")

    # 2) Discover md files (recursive)
    md_files = sorted(
    p for p in data_dir.rglob("*.md")
    if p.name.lower() != "readme.md"
)
    log(f"Found {len(md_files)} .md files under /data")
    for f in md_files:
        log(f" - {f.relative_to(base_dir)}")

    # 3) Read + chunk
    all_chunks: List[Chunk] = []
    for path in md_files:
        text = safe_read_text(path)
        chunks = safe_chunk(text, max_chars=800)
        log(f"{path.name}: {len(chunks)} chunks")

        # unicode smoke log (first 60 chars)
        if chunks:
            preview = chunks[0][:60].replace("\n", " ")
            log(f"  preview: {preview}")

        doc_id = path.stem
        for i, ch in enumerate(chunks):
            all_chunks.append(
                Chunk(
                    doc_id=doc_id,
                    chunk_id=f"{doc_id}::chunk{i:03d}",
                    text=ch,
                    source_path=str(path),
                )
            )

    log(f"Total chunks prepared: {len(all_chunks)}")
    if not all_chunks:
        log("No chunks to index. Exiting.")
        return

    # 4) Init Chroma (local)
    log("Initializing Chroma client...")
    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )

    # recreate collection (deterministic)
    try:
        client.delete_collection(collection_name)
        log("Deleted existing collection")
    except Exception:
        log("No existing collection to delete")

    col = client.create_collection(name=collection_name)

    # 5) Compute embeddings (with timing)
    texts = [c.text for c in all_chunks]
    ids = [c.chunk_id for c in all_chunks]
    metas = [{"doc_id": c.doc_id, "source_path": c.source_path} for c in all_chunks]

    log("Computing embeddings...")
    t0 = time.time()
    embeddings = embedder.encode(
        texts,
        show_progress_bar=True,
        batch_size=8,
    )
    log(f"Embeddings computed: {len(embeddings)} vectors in {time.time() - t0:.1f}s")

    # 6) Smoke test: write 1 item first (helps detect Unicode/storage issues fast)
    log("Chroma smoke test: adding 1 item...")
    col.add(
        ids=[ids[0]],
        documents=[texts[0]],
        metadatas=[metas[0]],
        embeddings=[embeddings[0].tolist()],
    )
    log("Smoke test OK (1 item added)")

    # 7) Add the rest (batch)
    if len(ids) > 1:
        log(f"Adding remaining {len(ids) - 1} items to Chroma...")
        col.add(
            ids=ids[1:],
            documents=texts[1:],
            metadatas=metas[1:],
            embeddings=[e.tolist() for e in embeddings[1:]],
        )

    # 8) Final verification
    count = col.count()
    log(f"Chroma collection count: {count}")

    log(f"Indexing done in {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
