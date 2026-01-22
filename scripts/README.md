# Scripts

This folder contains the core scripts for the AI Offer Assistant MVP.

## rag_index.py
Indexes synthetic product documentation into a local vector database (Chroma).
- Reads markdown files from /data
- Chunks documents
- Computes embeddings locally
- Stores vectors in Chroma (local-only)

## rag_query.py
Minimal integrity check for the vector database.
- Verifies that documents were indexed correctly

## rag_search.py (next step)
Performs semantic search:
- Customer email → embeddings
- Retrieves most relevant product documentation chunks
