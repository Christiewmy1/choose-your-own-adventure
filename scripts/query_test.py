"""
Run a natural-language similarity search against the local Chroma index.
Requires: python scripts/ingest_data.py first.
Run from repo root: python scripts/query_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

REPO_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = REPO_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "uwb_courses"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_QUERY = "Which courses cover teamwork, requirements, and testing in software projects?"


def main() -> None:
    if not CHROMA_DIR.is_dir():
        print(f"Index not found at {CHROMA_DIR}. Run: python scripts/ingest_data.py", file=sys.stderr)
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip() or DEFAULT_QUERY
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    results = store.similarity_search_with_score(query, k=4)

    print(f"Query: {query}\n")
    for i, (doc, score) in enumerate(results, start=1):
        code = doc.metadata.get("code", "")
        title = doc.metadata.get("title", "")
        print(f"--- Result {i} (distance ~ {score:.4f}) ---")
        print(f"{code}: {title}")
        print(doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else ""))
        print()


if __name__ == "__main__":
    main()
