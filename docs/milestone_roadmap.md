# Milestone Roadmap

This roadmap shows the planned sequence, actual completion evidence, and delivered artifacts. Dates are project-tracking dates for the CSS 382 Spring 2026 DYOP timeline.

| Milestone | Planned date | Actual completion date | Delivered evidence |
| --- | --- | --- | --- |
| Problem framing and proposal | 2026-05-03 | 2026-05-05 | Defined the UW Bothell advising problem, scoped the MVP around UWB course/career planning, and drafted `docs/final_project_spec.md`, `docs/system_overview.md`, and `docs/project_website_content.md`. |
| MVP recommendation engine | 2026-05-10 | 2026-05-12 | Built `src/huskyadvisor/advisor.py`, `src/huskyadvisor/json_data.py`, and initial JSON datasets in `data/` for courses, companies, internships, and roadmap templates. |
| Website and API integration | 2026-05-17 | 2026-05-20 | Added React/Vite frontend in `web/`, FastAPI backend in `api/`, API contract docs, and GitHub Pages deployment workflow. |
| AI/data pipeline expansion | 2026-05-22 | 2026-05-26 | Added Crawl4AI ingestion scripts, normalized/retrieval-ready data separation, Groq/Llama optional summary enhancement, and `ai_trace` response metadata. |
| Evaluation and dataset expansion | 2026-05-26 | 2026-05-28 | Expanded to 6 major pathways, 122 courses, 140 employers, company-course mappings, API contract tests, Crawl4AI tests, and advisor regression tests. |
| Final grading hardening | 2026-05-28 | 2026-05-28 | Added 560-scenario deep QA runner, demo-safe frontend fallback, API status badge, build timestamp, rubric alignment audit, and demo readiness checklist. |

## Final-mile tasks

- Refresh the public Vercel backend so it matches the latest `HuskyAdvisor` branch.
- Confirm the live site shows the newest AI trace and expanded-company behavior after deployment.
- Keep presentation wording honest: planning support only, not official UW advising.
