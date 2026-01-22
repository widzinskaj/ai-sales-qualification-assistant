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


def get_rag_context(
    email_text: str,
    top_k: int = 2,
    persist_dir: str = "chroma_db",
    collection_name: str = "bess_public",
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> str:
    """
    Returns ranked RAG context as plain text.
    No business logic, no interpretation.
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
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context_blocks = []

    for rank, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        source_name = Path(meta.get("source_path", "unknown")).name
        doc_id = meta.get("doc_id", "unknown")

        context_blocks.append(
            f"Rank {rank}\n"
            f"Source: {source_name}\n"
            f"Doc ID: {doc_id}\n"
            f"Excerpt:\n{doc.strip()}\n"
        )

    return "\n---\n".join(context_blocks)


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
