# Crawl4AI Integration Plan

## Purpose

This document explains how Crawl4AI fits into HuskyAdvisor as a data-ingestion layer. It does **not** replace the recommendation engine. Instead, it helps the project gather fresher UW Bothell and employer information that can later be cleaned and folded into the existing advising datasets.

## Why Crawl4AI Fits This Project

HuskyAdvisor already has:

- a recommendation engine
- structured JSON datasets
- an optional retrieval/vector path

What it lacks is a strong repeatable pipeline for pulling fresh public data from:

- UW Bothell major/program pages
- UWB time schedule pages
- employer about/careers pages

Crawl4AI is useful here because it produces LLM-friendly markdown and crawl metadata that can be reviewed, normalized, and then reused by both the structured advising engine and the optional retrieval flow.

## Architecture

```text
Public UWB / company pages
    ->
Crawl4AI raw crawl script
    ->
data/crawl4ai/raw/
    ->
normalization script
    ->
data/crawl4ai/normalized/
    ->
1. manual review into main JSON advising datasets
2. optional retrieval/vector ingestion
```

## Files Added

### Target manifest

- `data/crawl4ai/targets/seed_targets.json`

This file lists a small but high-value seed set of pages to crawl first:

- UWB major/program pages
- UWB schedule pages
- company/careers pages relevant to supported pathways

### Raw crawl runner

- `scripts/crawl_with_crawl4ai.py`

This script:

- loads the target manifest
- runs Crawl4AI against each target
- stores raw markdown and crawl metadata in `data/crawl4ai/raw/`

### Normalization step

- `scripts/normalize_crawl4ai_exports.py`
- `src/huskyadvisor/crawl4ai_pipeline.py`

These files convert raw Crawl4AI exports into:

- page summaries
- lightweight retrieval-ready document payloads

### Tests

- `tests/test_crawl4ai_pipeline.py`

These tests protect the normalization logic so the project can keep using the pipeline without silently breaking course-code extraction or page classification.

## Output Structure

### Raw data

- `data/crawl4ai/raw/<target-id>/page.json`
- `data/crawl4ai/raw/<target-id>/page.md`

This layer is intentionally close to the source and may contain noise. It should not be treated as final advising truth.

### Normalized data

- `data/crawl4ai/normalized/crawl4ai_page_summaries.json`
- `data/crawl4ai/normalized/crawl4ai_retrieval_documents.json`

This layer is easier to inspect and is a better bridge into:

- manual dataset refreshes
- retrieval/vector ingestion
- source traceability

## Honesty / Scope Notes

- Crawl4AI improves freshness, not certainty.
- Public web pages can change structure over time.
- Crawled content still needs validation before it becomes official advising data.
- The current MVP should still distinguish:
  - manually curated records
  - catalog/schedule-derived records
  - Crawl4AI-derived raw research material

## How This Strengthens The AI Story

HuskyAdvisor's optional retrieval path already includes vector-store and self-query components. Crawl4AI makes that path more credible because it provides:

- fresher web-derived text
- better source traceability
- a realistic way to refresh public university/company context

That makes the project's AI/data pipeline look less like a one-time hand-built demo and more like a real ingest-and-recommend system.

## Suggested Next Uses

1. Crawl several official UWB major pages and refresh `data/major_pathway_comparison.json`
2. Crawl quarterly time-schedule pages and expand schedule snapshots
3. Crawl top employer careers/about pages and strengthen `data/company_intent_profiles.json`
4. Feed normalized Crawl4AI documents into the retrieval/vector pipeline

## Basic Commands

After installing Crawl4AI:

```bash
pip install crawl4ai
crawl4ai-setup
PYTHONPATH=src python3 scripts/crawl_with_crawl4ai.py
PYTHONPATH=src python3 scripts/normalize_crawl4ai_exports.py
```
