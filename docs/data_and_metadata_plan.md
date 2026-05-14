# HuskyAdvisor Data and Metadata Plan

## Purpose

This document explains the data work behind HuskyAdvisor's MVP. It is especially useful for tracking the data/documentation contribution area of the project.

## Current Dataset Scope

The MVP dataset is a manually curated Spring 2026 snapshot that supports:

- CSSE major exploration
- Applied Computing major exploration
- EE major exploration
- 300-level preparation courses
- 400-level elective recommendations
- career alignment for systems, embedded, software, cloud, testing, and analytics pathways

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

For the MVP, accuracy matters more than scale. The project uses a smaller dataset that is easier to inspect manually instead of pretending to cover the entire university catalog.

Quality approach:

- prefer fewer but better-tagged records
- include transparent notes about scope and confidence
- keep the seed dataset editable in JSON
- expand only after fields are consistent

## Planned Expansions

- add more 400-level electives for each target major
- separate official university records from manually inferred tags
- add local employer records with skill mappings
- add source URLs where appropriate
- support data refresh workflows after the MVP
- add recent-offering signals from imported catalog snapshots

## Limitations

- the current dataset is not a complete or official advising source
- some tags are inferred from descriptions rather than copied from official metadata
- prerequisites are simplified for demo purposes

## Recommended Next Data Tasks

1. Add source URLs to high-priority course records
2. Expand Applied Computing course coverage
3. Add company-to-skill-to-course mappings
4. Add a few example quarter plans in structured JSON
5. Merge recent term availability from `uwb_recent_css_catalog_summary.json` into recommendation scoring
