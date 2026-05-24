from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from huskyadvisor.json_data import load_course_records
from huskyadvisor.vector_store import build_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "uwb_courses"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> None:
    courses = load_course_records()
    documents = build_documents(courses, [], [])
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
    print(f"Ingested {len(courses)} JSON-defined courses into {CHROMA_DIR}")


if __name__ == "__main__":
    main()
