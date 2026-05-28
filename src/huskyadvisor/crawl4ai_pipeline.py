from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


COURSE_CODE_PATTERN = re.compile(r"\b([A-Z]{2,5})\s*(\d{3})\b")
WHITESPACE_PATTERN = re.compile(r"\s+")


def slugify_target(url: str, label: str | None = None) -> str:
    parsed = urlparse(url)
    stem = label or parsed.path.strip("/") or parsed.netloc
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return cleaned or "root"


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", value).strip()


def extract_course_codes(*values: str) -> list[str]:
    codes: set[str] = set()
    for value in values:
        for department, level in COURSE_CODE_PATTERN.findall(value.upper()):
            codes.add(f"{department} {level}")
    return sorted(codes)


def infer_page_type(tags: list[str], url: str, title: str) -> str:
    normalized_tags = {tag.lower() for tag in tags}
    fingerprint = f"{url} {title}".lower()
    if "company" in normalized_tags or "careers" in normalized_tags:
        return "company"
    if "schedule" in normalized_tags or "timeschd" in fingerprint:
        return "schedule"
    if "major" in normalized_tags or "degree" in normalized_tags or "program" in fingerprint:
        return "major"
    if "course" in normalized_tags or "catalog" in normalized_tags:
        return "course"
    return "reference"


def build_summary_record(raw_payload: dict[str, Any]) -> dict[str, Any]:
    title = normalize_whitespace(raw_payload.get("title", "Untitled page"))
    markdown = raw_payload.get("markdown", "")
    excerpt = normalize_whitespace(markdown[:600])
    tags = raw_payload.get("tags", [])
    url = raw_payload["url"]
    return {
        "target_id": raw_payload["target_id"],
        "label": raw_payload.get("label", title),
        "url": url,
        "page_type": infer_page_type(tags, url, title),
        "title": title,
        "tags": tags,
        "course_codes": extract_course_codes(title, markdown),
        "markdown_excerpt": excerpt,
        "word_count": len(markdown.split()),
        "captured_at": raw_payload.get("captured_at"),
        "crawl_metadata": raw_payload.get("crawl_metadata", {}),
    }


def build_retrieval_document(raw_payload: dict[str, Any]) -> dict[str, Any]:
    summary = build_summary_record(raw_payload)
    body = normalize_whitespace(raw_payload.get("markdown", ""))
    return {
        "document_id": summary["target_id"],
        "url": summary["url"],
        "title": summary["title"],
        "page_type": summary["page_type"],
        "tags": summary["tags"],
        "course_codes": summary["course_codes"],
        "content": body[:8000],
    }


def load_raw_exports(raw_dir: Path) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for path in sorted(raw_dir.rglob("page.json")):
        with path.open(encoding="utf-8") as handle:
            payloads.append(json.load(handle))
    return payloads
