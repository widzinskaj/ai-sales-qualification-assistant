import os
import chromadb
from chromadb.config import Settings

def main():
    client = chromadb.PersistentClient(
        path=os.getenv("CHROMA_PERSIST_DIR", "chroma_db"),
        settings=Settings(anonymized_telemetry=False),
    )

    collection = client.get_collection(
        os.getenv("CHROMA_COLLECTION", "bess_public")
    )

    count = collection.count()
    print(f"\n[rag_query] Indexed chunks in DB: {count}\n")

if __name__ == "__main__":
    main()
