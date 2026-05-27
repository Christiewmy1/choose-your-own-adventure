"""
Run Crawl4AI against a small set of UW Bothell and employer pages and save
raw markdown + crawl metadata for later normalization.

Usage:
    PYTHONPATH=src python3 scripts/crawl_with_crawl4ai.py
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from huskyadvisor.crawl4ai_pipeline import slugify_target


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = PROJECT_ROOT / "data" / "crawl4ai" / "targets" / "seed_targets.json"
RAW_ROOT = PROJECT_ROOT / "data" / "crawl4ai" / "raw"


def load_targets() -> list[dict[str, Any]]:
    with TARGETS_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("targets", [])


def ensure_runtime() -> tuple[Any, Any, Any]:
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
    except ImportError as exc:  # pragma: no cover - runtime guard
        raise SystemExit(
            "Crawl4AI is not installed. Install it with `pip install crawl4ai` and run "
            "`crawl4ai-setup` before using this script."
        ) from exc
    return AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig


async def crawl_target(
    crawler: Any,
    crawler_run_config: Any,
    target: dict[str, Any],
) -> dict[str, Any]:
    result = await crawler.arun(url=target["url"], config=crawler_run_config)
    target_id = target.get("id") or slugify_target(target["url"], target.get("label"))
    captured_at = datetime.now(timezone.utc).isoformat()
    return {
        "target_id": target_id,
        "label": target.get("label", target["url"]),
        "url": target["url"],
        "tags": target.get("tags", []),
        "captured_at": captured_at,
        "title": getattr(result, "title", "") or target.get("label", target["url"]),
        "markdown": getattr(result, "markdown", "") or "",
        "raw_html": getattr(result, "html", "") or "",
        "crawl_metadata": {
            "success": getattr(result, "success", False),
            "status_code": getattr(result, "status_code", None),
            "links_count": len(getattr(result, "links", []) or []),
        },
    }


def save_payload(payload: dict[str, Any]) -> None:
    target_dir = RAW_ROOT / payload["target_id"]
    target_dir.mkdir(parents=True, exist_ok=True)

    page_json = target_dir / "page.json"
    markdown_file = target_dir / "page.md"
    source_file = target_dir / "source.txt"

    with page_json.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)

    markdown_file.write_text(payload["markdown"], encoding="utf-8")
    source_file.write_text(payload["url"] + "\n", encoding="utf-8")


async def main() -> None:
    AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig = ensure_runtime()
    targets = load_targets()
    RAW_ROOT.mkdir(parents=True, exist_ok=True)

    browser_config = BrowserConfig(headless=True, verbose=False)
    crawler_run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for target in targets:
            payload = await crawl_target(crawler, crawler_run_config, target)
            save_payload(payload)
            print(f"Saved {payload['target_id']} -> {payload['url']}")


if __name__ == "__main__":
    asyncio.run(main())
