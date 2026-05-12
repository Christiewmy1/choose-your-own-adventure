"""
Run a natural-language similarity search against the local Chroma index.
Uses data/student_profile.json to drop courses the student has already completed
so results favor new recommendations.

Requires: python scripts/ingest_data.py first.
Run from repo root: python scripts/query_test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

REPO_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = REPO_ROOT / "data" / "chroma_db"
PROFILE_PATH = REPO_ROOT / "data" / "student_profile.json"
COLLECTION_NAME = "uwb_courses"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_QUERY = "Which courses cover teamwork, requirements, and testing in software projects?"
RESULT_K = 4
FETCH_K = 32


def normalize_course_code(code: str) -> str:
    """Normalize catalog codes for set lookup."""
    return " ".join(str(code).strip().upper().split())


def load_completed_codes(path: Path) -> set[str]:
    if not path.is_file():
        print(
            f"Warning: profile not found at {path}; skipping completed-course filter.",
            file=sys.stderr,
        )
        return set()
    with path.open(encoding="utf-8") as f:
        profile = json.load(f)
    raw = profile.get("completed_course_codes", [])
    return {normalize_course_code(c) for c in raw}


def filter_out_completed(
    ranked: list[tuple[Document, float]], completed: set[str]
) -> list[tuple[Document, float]]:
    out: list[tuple[Document, float]] = []
    for doc, score in ranked:
        code = normalize_course_code(doc.metadata.get("code", ""))
        if code in completed:
            continue
        out.append((doc, score))
    return out


def main() -> None:
    if not CHROMA_DIR.is_dir():
        print(
            f"Index not found at {CHROMA_DIR}. Run: python scripts/ingest_data.py",
            file=sys.stderr,
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip() or DEFAULT_QUERY
    completed = load_completed_codes(PROFILE_PATH)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    candidates = store.similarity_search_with_score(query, k=FETCH_K)
    filtered = filter_out_completed(candidates, completed)
    results = filtered[:RESULT_K]

    print(f"Query: {query}\n")
    if completed:
        shown = ", ".join(sorted(completed))
        print(f"Excluding completed courses: {shown}\n")
    if not results:
        print(
            "No matches after removing completed courses. "
            "Try a broader query, clear completed_course_codes, or ingest more courses."
        )
        return

    for i, (doc, score) in enumerate(results, start=1):
        code = doc.metadata.get("code", "")
        title = doc.metadata.get("title", "")
        print(f"--- Result {i} (distance ~ {score:.4f}) ---")
        print(f"{code}: {title}")
        snippet = doc.page_content[:500]
        if len(doc.page_content) > 500:
            snippet += "..."
        print(snippet)
        print()


if __name__ == "__main__":
    main()
