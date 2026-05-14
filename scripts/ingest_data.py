"""
Load UWB course descriptions from JSON and build a persisted Chroma vector index.
Run from repo root: python scripts/ingest_data.py
"""

from __future__ import annotations

import json
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_JSON = REPO_ROOT / "data" / "uwb_courses_sample.json"
CHROMA_DIR = REPO_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "uwb_courses"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_courses(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)
    courses = payload.get("courses", [])
    if not courses:
        raise ValueError(f"No courses found in {path}")
    return courses


def courses_to_documents(courses: list[dict]) -> list[Document]:
    docs: list[Document] = []
    for c in courses:
        code = c.get("code", "")
        title = c.get("title", "")
        desc = c.get("description", "")
        page = f"{code}: {title}\n\n{desc}".strip()
        meta = {
            "code": code,
            "title": title,
            "credits": c.get("credits"),
            "department": c.get("department", ""),
        }
        docs.append(Document(page_content=page, metadata=meta))
    return docs


def main() -> None:
    if not DATA_JSON.is_file():
        raise FileNotFoundError(f"Missing sample data: {DATA_JSON}")

    courses = load_courses(DATA_JSON)
    documents = courses_to_documents(courses)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    splits = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    print(f"Ingested {len(courses)} courses ({len(splits)} chunks) into {CHROMA_DIR}")


if __name__ == "__main__":
    main()
