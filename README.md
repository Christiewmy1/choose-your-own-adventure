# HuskyAdvisor

HuskyAdvisor is a UW Bothell-focused advising web application that helps students compare majors, discover career-aligned courses, connect coursework to regional employers, and generate internship-prep and roadmap guidance.

## Public deliverables

- Public website: [https://christiewmy1.github.io/choose-your-own-adventure/](https://christiewmy1.github.io/choose-your-own-adventure/)
- Deployed API target: `https://choose-your-own-adventure-bay.vercel.app`
- Local frontend: `web/`
- Local/deployed backend: `api/`
- Core recommendation engine: `src/huskyadvisor/`

If the public site appears stale, GitHub Pages caching may be the cause. The current website is built from `web/` and published by `.github/workflows/deploy-web.yml`.

## Why this project matters to UW

UW Bothell students often gather planning advice from scattered places: catalog pages, degree sheets, internship listings, faculty suggestions, and career fair notes. HuskyAdvisor packages that information into one UWB-specific experience so students can get more actionable guidance about:

- which major pathway fits their interests
- which courses match their goals
- which local employers align with those courses
- what they should do next for internship readiness

## AI integration

HuskyAdvisor is not a chat box bolted onto a website. AI is embedded in the recommendation logic in two ways:

1. A structured advising engine scores majors, courses, company pathways, and roadmap tracks using student profile features, prerequisite readiness, company intent, and career-tag alignment.
2. An optional retrieval-augmented path uses LangChain, Chroma, and OpenAI-backed retrieval modules for a richer LLM-grounded demo flow.

The current deployed MVP primarily uses the structured advising engine because it is more stable for a class demo, but the repository also includes the retrieval modules that support the broader AI strategy.

The repo now also includes a Crawl4AI-based ingestion pipeline for gathering fresh public UWB and employer source pages before they are normalized into retrieval documents or manually refreshed into the core advising datasets.

## Current shipped architecture

The current student-facing flow is:

`React website -> FastAPI API -> HuskyAdvisorEngine -> JSON datasets -> recommendation results`

Main production-oriented entry points:

- Website entry: `web/src/App.tsx`
- API entry: `api/main.py`
- Recommendation engine: `src/huskyadvisor/advisor.py`
- Data loading: `src/huskyadvisor/json_data.py`

The older CLI prototype still exists for direct testing, but it is no longer the main user-facing flow.

## What currently works

- public website shell hosted on GitHub Pages
- FastAPI backend for profile recommendations, companies, internship prep, roadmap, and major suggestion
- 6 supported major pathways:
  - CSSE
  - Applied Computing
  - EE
  - Computer Engineering
  - Data Visualization
  - technology-facing Business Administration
- 122 course records in the main advising dataset
- 120 company targets in the company dataset
- completed-course filtering so already taken courses are not recommended again
- company-aware internship-prep and roadmap matching
- stress-test coverage across 58 simulated student profiles
- regression coverage for core advising flows

## Current limitations

HuskyAdvisor is still an MVP, not an official UW advising system.

It does not currently provide:

- official advisor-approved degree clearance
- live internship scraping
- real-time schedule integration in the public app
- full major coverage for every UW Bothell department

The strongest support is still in computing and engineering-oriented pathways.

## Local development

### Backend

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project
PYTHONPATH=src uvicorn api.main:app --host 127.0.0.1 --port 8010
```

Health check:

```bash
curl http://127.0.0.1:8010/health
```

### Frontend

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/web
npm install
npm run dev
```

The frontend uses:

- `http://127.0.0.1:8010` when running locally
- `https://choose-your-own-adventure-bay.vercel.app` as the default deployed API target

## Repository structure

### Main application code

- `api/`
  - deployed FastAPI service used by the website
- `src/huskyadvisor/`
  - recommendation logic, models, loaders, optional retrieval path
- `web/`
  - React/Vite student-facing interface

### Main data

- `data/uwb_courses_sample.json`
- `data/local_tech_companies.json`
- `data/company_course_mapping.json`
- `data/company_intent_profiles.json`
- `data/internship_prep_playbooks.json`
- `data/quarter_plan_templates.json`
- `data/major_pathway_comparison.json`
- `data/crawl4ai/`
  - raw crawl exports
  - normalized Crawl4AI summaries
  - target manifests

### Key project docs

- [docs/final_project_spec.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/final_project_spec.md)
- [docs/ai_integration_strategy.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/ai_integration_strategy.md)
- [docs/deployment_and_public_access.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/deployment_and_public_access.md)
- [docs/milestone_roadmap.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/milestone_roadmap.md)
- [docs/rubric_alignment_audit.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/rubric_alignment_audit.md)
- [docs/system_overview.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/system_overview.md)
- [docs/technical_design_document.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/technical_design_document.md)
- [docs/crawl4ai_integration.md](/Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project/docs/crawl4ai_integration.md)

## Deployment notes

- GitHub Pages deployment for the website is defined in `.github/workflows/deploy-web.yml`
- Vercel deployment for the API is defined in `vercel.json`
- `render.yaml` remains as an alternate deployment template, but the verified public API target is Vercel.
- No password-protected flow is currently required for the public demo

## Testing

Run the full automated Python test suite from the repository root:

```bash
python3 -m unittest discover
```

Build-check the public website:

```bash
cd web
npm run build
```

Core backend regression tests live in:

- `tests/test_advisor_regression.py`
- `tests/test_api_contract.py`

Stress-test reporting lives in:

- `scripts/generate_simulation_report.py`
- `docs/simulation_test_matrix.md`
- `docs/simulation_coverage_report.md`

## Important repository hygiene note

Generated frontend artifacts such as `web/node_modules/` and `web/dist/` should not be committed as source. They are ignored in `.gitignore` and have been removed from version control tracking.
