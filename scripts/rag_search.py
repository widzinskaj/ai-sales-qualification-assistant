import os
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


def log(msg: str) -> None:
    print(f"[rag_search] {msg}", flush=True)


def load_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {path}")
    return text


def shorten(text: str, max_chars: int = 300) -> str:
    """
    Hard cut for readability.
    No summarization, no interpretation.
    """
    text = text.strip().replace("\n", " ")
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


def extract_overlap(query: str, doc: str, max_terms: int = 5) -> list[str]:
    """
    Pure token overlap.
    Diagnostic only, not used for decisions.
    """
    q_terms = set(query.lower().split())
    d_terms = set(doc.lower().split())
    overlap = sorted(q_terms & d_terms)
    return overlap[:max_terms]


def get_rag_context(
    email_text: str,
    top_k: int = 2,
    persist_dir: str = "chroma_db",
    collection_name: str = "bess_public",
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> str:
    """
    Returns short, comparable RAG context blocks.
    - 1 block per document (deduplicated by doc_id)
    - No business logic
    - No interpretation
    """

    embedder = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_collection(collection_name)

    query_embedding = embedder.encode([email_text])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    context_blocks = []

    seen_docs: set[str] = set()
    rank = 1

    for doc, meta, dist in zip(documents, metadatas, distances):
        doc_id = meta.get("doc_id", "unknown")

        # Deduplicate: 1 document = 1 RAG block
        if doc_id in seen_docs:
            continue

        seen_docs.add(doc_id)

        source_name = Path(meta.get("source_path", "unknown")).name
        overlap_terms = extract_overlap(email_text, doc)

        context_blocks.append(
            f"[RAG-{rank}]\n"
            f"Source: {source_name}\n"
            f"Doc ID: {doc_id}\n"
            f"Distance: {dist:.3f}\n"
            f"Overlap terms: {', '.join(overlap_terms) if overlap_terms else 'n/a'}\n"
            f"Excerpt:\n\"{shorten(doc)}\""
        )

        rank += 1

    return "\n\n---\n\n".join(context_blocks)


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    email_file = os.getenv("RAG_EMAIL_FILE", "client_email_01.txt")
    email_path = base_dir / "queries" / email_file

    log(f"Loading customer email from: {email_path}")
    customer_email = load_text(email_path)

    log("Running RAG search...")
    rag_context = get_rag_context(customer_email, top_k=2)

    print("\n=== RAG CONTEXT ===\n")
    print(rag_context)
    print("\n=== END ===\n")


if __name__ == "__main__":
    main()
