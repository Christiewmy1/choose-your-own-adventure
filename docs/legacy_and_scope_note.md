# Legacy And Scope Note

## Why This Note Exists

The HuskyAdvisor repository lives on a branch inside a forked repository that originally came from a different project. Because of that, the repository history and file tree can be confusing unless the current project scope is stated clearly.

## Current HuskyAdvisor Scope

HuskyAdvisor is the current project focus. Its MVP is an AI-assisted advising prototype for UW Bothell students that provides:

- major guidance
- course recommendations
- local company alignment
- internship-preparation guidance

The current MVP is centered on:

- `src/huskyadvisor/`
- `data/`
- `docs/`

## Legacy / Reference Material

Some repository content should be treated as legacy, inherited, or reference-only:

- `external_huskyadvisor/`
  - copied reference material used during project integration
- older non-HuskyAdvisor prototype or fork artifacts
  - useful for background, but not the main MVP path

These files may still be present in the branch history, but they are not the main product story.

## How To Read The Repository

If you are reviewing HuskyAdvisor, use this order:

1. `README.md`
2. `docs/system_overview.md`
3. `src/huskyadvisor/main.py`
4. `data/` JSON files
5. `docs/technical_design_document.md`

## Simple Scope Rule

If a file directly supports:

- student profile input
- UWB course/company datasets
- recommendation logic
- company alignment
- internship preparation

then it is part of the active HuskyAdvisor MVP.

If it mainly relates to older fork history or copied reference material, it should be treated as supporting or legacy context unless the team explicitly reuses it.
