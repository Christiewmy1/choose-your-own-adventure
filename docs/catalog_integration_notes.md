# Catalog Integration Notes

## Source Used

- Source URL: [catalog.json](https://github.com/pisanuw/01shortAIproject/blob/main/data/catalog.json)
- Derived snapshot imported on: 2026-05-14

## What This Source Contains

The external catalog contains a large set of CSS course offerings across multiple terms, including section and instructor information. In the imported snapshot, it spans from Autumn 2020 through Spring 2026 and includes a broad list of UWB CSS course records.

## Why It Helps HuskyAdvisor

This source is useful because it adds a stronger sense of:

- which courses are actually offered in recent academic terms
- which 300- and 400-level courses appear repeatedly
- which electives seem active enough to mention in planning recommendations

For HuskyAdvisor, this means the project can move from a purely hand-written sample list toward a more evidence-based dataset.

## How It Was Used

For the current project stage, the source was not copied directly into the main recommendation engine as raw truth. Instead, it was summarized into:

- `data/uwb_recent_css_catalog_summary.json`

That summary keeps only the parts most useful for advising:

- course code
- course title
- recent offering terms
- a short advising note

## Why We Chose A Summary Layer

The raw source includes many records for repeated sections and terms. That is helpful for analysis, but not ideal for a small MVP recommendation engine. A summarized layer is easier to inspect, easier to explain in class, and safer to integrate without cluttering the core dataset.

## Good Next Uses

- merge recent offering terms into the main seed dataset
- prioritize electives that appeared in AUT2025, WIN2026, or SPR2026
- add a simple "recently offered" signal to HuskyAdvisor recommendations
- compare stable recurring courses against one-off special topics

## Matiyas Contribution Framing

This work fits the data/documentation lead role because it:

- expands the project's data foundation
- documents an external source clearly
- turns a raw catalog into a structured advising asset
- prepares the dataset for future integration into the recommendation logic
