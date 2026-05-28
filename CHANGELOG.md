# Changelog

## 2026-05-28

- Added a 560-profile deep QA stress test in `scripts/run_deep_qa.py`.
- Added `docs/deep_qa_500_scenario_report.md` with scenario, API, data, and deployment findings.
- Expanded the company dataset to 140 employers, including Fortune 500 and software-heavy employers.
- Added auditable `ai_trace` metadata to recommendation responses and displayed it in the frontend.
- Added a demo-safe fallback dashboard so the live presentation does not collapse on temporary API failure.
- Added API contract tests and made `python3 -m unittest discover` work from the repo root.
- Pointed the frontend to the working Vercel backend URL.

## 2026-05-26

- Added Crawl4AI ingestion and normalization scripts.
- Added docs explaining raw crawled data, normalized advising data, and retrieval-ready documents.
- Added Crawl4AI pipeline tests for course-code extraction, page typing, metadata handling, and retrieval document generation.

## 2026-05-23

- Added company-course mappings, company intent profiles, internship prep playbooks, and roadmap templates.
- Improved completed-course filtering and scope-warning honesty.
- Added major pathway comparison data for supported UWB pathways.

## 2026-05-20

- Connected the React/Vite frontend to FastAPI profile endpoints.
- Added result tabs for courses, companies, internship prep, and roadmap output.
- Added public deployment documentation for GitHub Pages and the backend API.

## 2026-05-12

- Built the initial HuskyAdvisor recommendation engine.
- Added JSON course/company loaders and core advising models.
- Created initial sample datasets for UWB-focused course and company planning.
