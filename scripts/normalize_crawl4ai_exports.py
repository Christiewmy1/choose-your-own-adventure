"""
Normalize raw Crawl4AI page exports into lightweight summary and retrieval files.

Usage:
    PYTHONPATH=src python3 scripts/normalize_crawl4ai_exports.py
"""

from __future__ import annotations

import json
from pathlib import Path

from huskyadvisor.crawl4ai_pipeline import (
    build_retrieval_document,
    build_summary_record,
    load_raw_exports,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = PROJECT_ROOT / "data" / "crawl4ai" / "raw"
NORMALIZED_ROOT = PROJECT_ROOT / "data" / "crawl4ai" / "normalized"
SUMMARY_PATH = NORMALIZED_ROOT / "crawl4ai_page_summaries.json"
RETRIEVAL_PATH = NORMALIZED_ROOT / "crawl4ai_retrieval_documents.json"


def main() -> None:
    payloads = load_raw_exports(RAW_ROOT)
    if not payloads:
        raise SystemExit(
            f"No raw Crawl4AI exports found in {RAW_ROOT}. Run scripts/crawl_with_crawl4ai.py first."
        )

    summaries = [build_summary_record(payload) for payload in payloads]
    retrieval_documents = [build_retrieval_document(payload) for payload in payloads]

    NORMALIZED_ROOT.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w", encoding="utf-8") as handle:
        json.dump({"pages": summaries}, handle, indent=2, ensure_ascii=True)

    with RETRIEVAL_PATH.open("w", encoding="utf-8") as handle:
        json.dump({"documents": retrieval_documents}, handle, indent=2, ensure_ascii=True)

    print(f"Wrote {len(summaries)} normalized page summaries to {SUMMARY_PATH}")
    print(f"Wrote {len(retrieval_documents)} retrieval documents to {RETRIEVAL_PATH}")


if __name__ == "__main__":
    main()
