# HuskyAdvisor Data and Metadata Plan

## Purpose

This document explains the data work behind HuskyAdvisor's MVP. It is especially useful for tracking the data/documentation contribution area of the project.

## Current Dataset Scope

The MVP dataset now combines:

- a manually curated advising-focused subset
- a broader catalog/schedule-derived CSS expansion layer

Together, these support:

- CSSE major exploration
- Applied Computing major exploration
- EE major exploration
- 300-level preparation courses
- 400-level elective recommendations
- career alignment for systems, embedded, software, cloud, testing, and analytics pathways

The project now also has a separate Crawl4AI ingestion layer for gathering fresh public source material before it is manually normalized into the core advising dataset.

## Current Record Fields

Each course record may include:

- `code`
- `title`
- `credits`
- `department`
- `level`
- `majors`
- `career_tags`
- `prerequisites`
- `project_emphasis`
- `description`
- `source_type`
- `source_confidence`

## Why These Fields Matter

- `majors` helps the system avoid recommending courses that do not fit the student's program
- `career_tags` helps connect classes to fields like aerospace, cloud, testing, and embedded systems
- `prerequisites` helps the app warn students about readiness
- `project_emphasis` helps later versions match students to project-heavy or lighter courses
- `source_confidence` makes it easier to be honest about what is official versus manually curated

## Data Quality Strategy

For the MVP, accuracy still matters more than scale, but the project now balances:

- a smaller set of higher-confidence curated records
- a larger set of lower-confidence catalog-derived records used to broaden coverage

Quality approach:

- clearly distinguish curated records from broader derived records
- include transparent notes about scope and confidence
- keep the seed dataset editable in JSON
- refine high-value records first, then gradually improve the broader catalog layer
- keep Crawl4AI raw exports separate from the cleaned advising JSON

## Planned Expansions

- add more 400-level electives for each target major
- separate official university records from manually inferred tags
- add local employer records with skill mappings
- add source URLs where appropriate
- support data refresh workflows after the MVP
- add recent-offering signals from imported catalog snapshots
- use Crawl4AI to refresh selected UWB major, schedule, and employer pages

## Limitations

- the current dataset is not a complete or official advising source
- some tags are inferred from descriptions rather than copied from official metadata
- prerequisites are simplified for demo purposes
- many catalog-derived records use placeholder metadata and should not be treated as equally detailed as the curated subset

## Recommended Next Data Tasks

1. Add source URLs to high-priority course records
2. Expand Applied Computing course coverage
3. Add company-to-skill-to-course mappings
4. Add a few example quarter plans in structured JSON
5. Merge recent term availability from `uwb_recent_css_catalog_summary.json` into recommendation scoring
