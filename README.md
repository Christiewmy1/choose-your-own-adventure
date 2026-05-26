# HuskyAdvisor

HuskyAdvisor is an AI-powered academic and career guidance prototype for **University of Washington Bothell** students. Its current MVP helps students compare majors, choose useful electives, connect coursework to local company pathways, and generate internship-preparation next steps using UWB-specific data.

## Live website

**Public demo:** [https://christiewmy1.github.io/choose-your-own-adventure/](https://christiewmy1.github.io/choose-your-own-adventure/)

The student-facing UI lives in `web/` (React + Vite). Pushes to the `main` branch rebuild and publish to the **`gh-pages`** branch via [GitHub Actions](.github/workflows/deploy-web.yml) (this repo’s Pages source).

### Run the website locally

```bash
cd web
npm install
npm run dev
```

Then open **http://localhost:4173** (profile form → course recommendations → company alignment).

## What This Repository Is

This repository hosts the **HuskyAdvisor** team project. The most important project code and data for the current MVP live in:

- `src/huskyadvisor/`
- `data/`
- `docs/`

If you are trying to understand the current project, start there.

## What This Repository Is Not

This repository was originally forked from another project and still contains some older or inherited files. Those legacy or reference materials are **not** the main HuskyAdvisor MVP. In particular:

- `external_huskyadvisor/` is a copied reference import used during project integration
- some older scripts in `scripts/` came from an earlier prototype path
- the current HuskyAdvisor logic does **not** depend on the old choose-your-own-adventure/book-processing history

For a clearer explanation, see:

- [docs/legacy_and_scope_note.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/legacy_and_scope_note.md)
- [docs/system_overview.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/system_overview.md)

## Current MVP Scope

The current HuskyAdvisor MVP focuses on:

- major guidance for UWB students
- elective recommendations
- local company alignment
- internship-preparation guidance
- explainable recommendations based on structured UWB-style data

The current MVP does **not** yet provide:

- live internship postings
- real-time job scraping
- official advisor-approved degree planning
- a fully polished public website (a working MVP is at the [live demo](https://christiewmy1.github.io/choose-your-own-adventure/); backend integration is still in progress)

## Demo Modes

The current working demo is a CLI prototype.

Run from the project root:

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project
PYTHONPATH=src python3 -m huskyadvisor.main --mode profile-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode company-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode internship-demo
PYTHONPATH=src python3 -m huskyadvisor.main --mode roadmap-demo
```

What each mode does:

- `profile-demo`: recommends courses based on a student profile
- `company-demo`: suggests local companies that align with a student's path
- `internship-demo`: gives a preparation plan with courses, project ideas, and skill focus
- `roadmap-demo`: gives a structured quarter-by-quarter plan using curated roadmap templates

## Project Structure

### Main HuskyAdvisor Code

- `src/huskyadvisor/main.py`
  - entrypoint for the CLI demo
- `src/huskyadvisor/advisor.py`
  - main recommendation logic
- `src/huskyadvisor/json_data.py`
  - loads structured JSON datasets
- `src/huskyadvisor/models.py`
  - data models
- `src/huskyadvisor/formatter.py`
  - output formatting

### Main HuskyAdvisor Data

- `data/student_profile.json`
  - sample student profile
- `data/uwb_courses_sample.json`
  - curated UWB course dataset
- `data/local_tech_companies.json`
  - local company dataset
- `data/company_course_mapping.json`
  - explicit company-to-course recommendations
- `data/internship_prep_playbooks.json`
  - internship-prep tracks
- `data/uwb_recent_css_catalog_summary.json`
  - summary derived from a larger UWB course catalog source
- `data/quarter_plan_templates.json`
  - structured roadmap templates for quarter-by-quarter planning
- `data/uwb_spring_2026_schedule_snapshot.json`
  - official Spring 2026 schedule snapshot with real sections and meeting times
- `data/uwb_2026_multi_quarter_schedule_snapshot.json`
  - official multi-quarter 2026 schedule snapshot across winter, spring, summer, and autumn

### Key Documentation

- `docs/technical_design_document.md`
  - system and architecture design
- `docs/system_overview.md`
  - execution flow and file-level overview
- `docs/frontend_handoff.md`
  - page-by-page guidance for the website team
- `docs/website_testing_checklist.md`
  - practical checklist for testing the website MVP
- `docs/website_copy_blocks.md`
  - ready-to-use page copy for the frontend MVP
- `docs/persona_test_matrix.md`
  - expected behavior for sample student scenarios
- `docs/data_coverage_audit.md`
  - honest summary of where the current dataset is strong and weak
- `docs/team_dependency_tracker.md`
  - clear handoff and ownership notes across data, frontend, and backend work
- `docs/matiyas_role_summary.md`
  - concise explanation of the data/documentation contribution lane
- `docs/api_contract.md`
  - proposed JSON response contract for the eventual website/backend connection
- `docs/frontend_gap_review.md`
  - current review of what the website does and what is still missing
- `docs/official_schedule_expansion_notes.md`
  - notes on the new official UW Bothell schedule snapshot
- `docs/multi_quarter_schedule_notes.md`
  - notes on the broader 2026 multi-quarter schedule dataset
- `docs/project_website_content.md`
  - content draft for the public project website
- `docs/data_and_metadata_plan.md`
  - metadata and dataset strategy
- `docs/evaluation_question_bank.md`
  - test prompts for recommendation quality
- `docs/manual_evaluation_report.md`
  - first-pass manual review of current demo quality
- `docs/source_reference_index.md`
  - transparency notes about where project data came from
- `docs/catalog_integration_notes.md`
  - external catalog integration notes

### Sample Personas For Testing

- `data/sample_student_personas.json`
  - reusable student cases for demo and website testing

## Optional LLM / RAG Path

There is also an optional LangChain/OpenAI path for a retrieval-based demo. That path uses:

- `src/huskyadvisor/vector_store.py`
- `src/huskyadvisor/retrieval.py`

It is secondary to the local CLI MVP and requires extra dependencies and an API key.

## Quick Start

1. Install dependencies.
2. Run one of the local demo modes.

Example:

```bash
PYTHONPATH=src python3 -m huskyadvisor.main --mode profile-demo
```

## Team Contribution Notes

The data/documentation contribution area is most visible in:

- `data/uwb_courses_sample.json`
- `data/local_tech_companies.json`
- `data/company_course_mapping.json`
- `data/internship_prep_playbooks.json`
- `docs/data_and_metadata_plan.md`
- `docs/project_website_content.md`
- `docs/system_overview.md`
- `docs/evaluation_question_bank.md`
- `docs/manual_evaluation_report.md`
- `docs/source_reference_index.md`
- `docs/frontend_handoff.md`
- `docs/website_testing_checklist.md`
- `docs/website_copy_blocks.md`
- `docs/persona_test_matrix.md`
- `docs/data_coverage_audit.md`
- `docs/team_dependency_tracker.md`
- `docs/matiyas_role_summary.md`
- `docs/api_contract.md`
- `docs/frontend_gap_review.md`
- `docs/official_schedule_expansion_notes.md`
- `docs/multi_quarter_schedule_notes.md`

## Next Major Step

The next major milestone is turning the current recommendation engine into a fully connected **student-facing website**. The backend and data layers are now strong enough that frontend work should continue using the live API instead of placeholder rules, while the team keeps improving data quality and evaluation coverage.

## Prototype API

The repository now includes a first-pass FastAPI layer for turning HuskyAdvisor into a website-backed product.

- API app: `src/huskyadvisor/api_app.py`
- Request models: `src/huskyadvisor/api_models.py`
- Shared advisor builder: `src/huskyadvisor/service.py`
- Quickstart: `docs/api_quickstart.md`

Planned local run command:

```bash
PYTHONPATH=src uvicorn huskyadvisor.api_app:app --host 127.0.0.1 --port 8010
```
