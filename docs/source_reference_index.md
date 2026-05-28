# HuskyAdvisor Source Reference Index

## Purpose

This document tracks where key HuskyAdvisor datasets came from and how they should be interpreted. It helps the project stay honest about which pieces are manually curated, which are derived from public sources, and which are inferred for advising purposes.

## Core Dataset Sources

### `data/uwb_courses_sample.json`

**Type:** Manually curated MVP seed dataset  
**Role:** Main academic recommendation dataset  
**Trust level:** Medium to high depending on record

This is the primary course dataset used by the HuskyAdvisor engine. It combines manually written course summaries, prerequisite notes, major tags, and career tags designed for recommendation quality rather than official advising use.

### `data/uwb_recent_css_catalog_summary.json`

**Type:** Derived summary dataset  
**Role:** Recent-offering signal for CSS courses  
**Trust level:** Medium-high

**Primary source:**  
[catalog.json](https://github.com/pisanuw/01shortAIproject/blob/main/data/catalog.json)

This dataset summarizes recently offered 300- and 400-level CSS courses and helps HuskyAdvisor prefer courses that appeared in recent terms.

### `data/imports/uwb_catalog_source.json`

**Type:** Raw imported source file  
**Role:** Traceability and catalog analysis  
**Trust level:** Medium-high

**Primary source:**  
[catalog.json](https://github.com/pisanuw/01shortAIproject/blob/main/data/catalog.json)

This file is kept as a raw reference import. It is not used directly by the main recommendation engine.

### `data/local_tech_companies.json`

**Type:** Manually curated company dataset  
**Role:** Local company alignment  
**Trust level:** Medium

This dataset represents plausible regional employers and target skill areas. It is meant for guidance and demo use, not as live recruiting data.

### `data/crawl4ai/raw/`

**Type:** Raw crawl exports  
**Role:** Source gathering for future refreshes and retrieval context  
**Trust level:** Variable

This folder stores raw Crawl4AI exports from selected UWB and employer pages. These exports are intentionally kept separate from the main recommendation dataset because they may include noise, formatting artifacts, or incomplete extractions that still require validation.

### `data/crawl4ai/normalized/`

**Type:** Normalized crawl summaries  
**Role:** Bridge layer between raw crawled pages and HuskyAdvisor-ready data  
**Trust level:** Medium

These files summarize Crawl4AI outputs into page-level records and retrieval-ready text documents. They are useful for manual review, vector-store ingestion, and future dataset refresh work.

### `data/company_course_mapping.json`

**Type:** Manually inferred mapping  
**Role:** Explicit company-to-course recommendation boost  
**Trust level:** Medium

These mappings are advising heuristics created for the MVP and are not official company endorsements.

### `data/internship_prep_playbooks.json`

**Type:** Manually designed planning dataset  
**Role:** Internship-preparation guidance  
**Trust level:** Medium

This file provides structured next-step planning for likely internship pathways. It is not based on live internship feeds.

## Recommended Transparency Language

When presenting HuskyAdvisor, use wording like:

“Some records in the MVP are curated and inferred for advising support rather than pulled from a fully automated official university pipeline. The project prioritizes explainability and usefulness over pretending the dataset is complete.”

## Good Next Source Improvements

1. Add official UWB URLs to high-priority course records
2. Separate official facts from inferred tags more explicitly
3. Add refresh dates to company and internship-prep datasets
4. Expand Applied Computing and EE source notes further
5. Use Crawl4AI exports to refresh public source material on a scheduled basis
