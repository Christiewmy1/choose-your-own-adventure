# Rubric Alignment Audit

## Purpose

This document maps HuskyAdvisor directly to the DYOP rubric from a strict-grader perspective. It is intentionally evidence-based: each category lists what is implemented, where to inspect it, and what the honest limitation is.

## Scorecard Target

| Rubric category | Points | Current evidence target |
| --- | ---: | --- |
| UW Community Impact | 10 | UWB-specific advising, major comparison, course planning, local employer alignment |
| AI Integration | 15 | Embedded recommendation engine, Groq/Llama enhancement, Crawl4AI ingestion, optional retrieval path |
| Technical Execution | 25 | React + FastAPI + tested recommendation engine + deployed API + demo fallback |
| Project Web Presence | 15 | Public GitHub Pages site, professional UI, user guide, architecture and deployment docs |
| Milestones & Planning | 20 | Proposal/spec docs, roadmap, audits, simulation reports, final readiness checklist |
| Peer Review | 15 | Contribution docs and teammate-facing evidence, with final score dependent on Canvas survey |

## 1. UW Community Impact

Status: **Excellent**

Evidence:

- The problem is specific to UW Bothell students who need course, major, roadmap, and internship-prep guidance.
- The app supports UWB-oriented pathways instead of generic national degree advice.
- The company layer focuses on regional employers and pathways students might realistically target.
- Public-facing explanation appears in `README.md`, `docs/final_project_spec.md`, and the website UI.

Honest limitation:

- HuskyAdvisor is strongest for computing, engineering, data, and technology-facing business pathways. It does not claim full-campus advising coverage.

## 2. AI Integration

Status: **Excellent**

Evidence:

- `src/huskyadvisor/advisor.py` provides embedded recommendation logic for courses, majors, companies, internship prep, and roadmaps.
- `api/llm.py` uses Groq/Llama 3.3 for optional personalized rewriting when a `GROQ_API_KEY` is configured.
- `src/huskyadvisor/crawl4ai_pipeline.py`, `scripts/crawl_with_crawl4ai.py`, and `scripts/normalize_crawl4ai_exports.py` provide a Crawl4AI data-ingestion pipeline.
- `src/huskyadvisor/vector_store.py` and retrieval-related docs explain how crawled/normalized documents strengthen the optional RAG path.
- Every API result includes an `ai_trace` field, and the website displays an "AI integration trace" so graders can see the engine, Groq/Llama status, Crawl4AI/data role, retrieval readiness, and fallback status for the exact result being shown.
- AI is part of the actual recommendation flow and data pipeline, not a separate side chat.

Honest limitation:

- Scraped content is treated as raw/normalized input that still needs validation before becoming trusted advising data.

## 3. Technical Execution

Status: **Strong**

Evidence:

- React/Vite frontend in `web/`.
- FastAPI backend in `api/`.
- Core Python recommendation engine in `src/huskyadvisor/`.
- JSON datasets are separated by courses, companies, company intent, internship playbooks, roadmap templates, major comparisons, schedule snapshots, and Crawl4AI data.
- `tests/test_advisor_regression.py` covers recommendation quality, completed-course filtering, scope honesty, company alignment, and major differentiation.
- `tests/test_crawl4ai_pipeline.py` covers Crawl4AI normalization edge cases.
- `tests/test_api_contract.py` verifies the public API contract shape.
- The frontend now has a clearly labeled demo-safe fallback if the deployed API is temporarily unavailable.

Honest limitation:

- The public app is still an MVP. It should not be represented as an official UW advising system.

## 4. Project Web Presence

Status: **Strong**

Evidence:

- Public website: `https://christiewmy1.github.io/choose-your-own-adventure/`
- API health check: `https://huskyadvisor-api-matiyas.vercel.app/health`
- The website explains the project, collects a student profile, and displays courses, companies, internship prep, and roadmap results.
- `docs/deployment_and_public_access.md` gives the public URLs and deployment architecture.
- `docs/demo_readiness_checklist.md` gives the exact demo profile and readiness checks.

Honest limitation:

- GitHub Pages can cache stale static assets briefly after deployment, so the team should hard-refresh before presenting.

## 5. Milestones and Planning

Status: **Strong**

Evidence:

- `docs/milestone_roadmap.md`
- `docs/final_project_spec.md`
- `docs/technical_design_document.md`
- `docs/manual_evaluation_report.md`
- `docs/simulation_test_matrix.md`
- `docs/simulation_coverage_report.md`
- `docs/data_coverage_audit.md`
- `docs/demo_readiness_checklist.md`

Honest limitation:

- Some planning artifacts were refined late in the project, so the presentation should emphasize iteration and final stabilization rather than pretending the architecture was perfect from day one.

## 6. Peer Review

Status: **Externally graded**

Evidence:

- `docs/matiyas_role_summary.md`
- `docs/matiyas_weekly_contribution_log.md`
- Commit history and merged code changes
- AI pipeline, backend fixes, frontend deployment fixes, testing, and documentation updates

Honest limitation:

- Final peer-review points depend on teammate Canvas submissions, not repository contents alone.

## Strict-Grader Readiness Summary

HuskyAdvisor now has a defensible path to a very high score because the repository shows:

- a real UW community problem
- AI embedded in recommendation and data-ingestion workflows
- a deployed frontend and verified backend
- automated regression, Crawl4AI, and API contract tests
- honest limitations and clear scope warnings
- public documentation and demo-readiness materials

The final presentation should focus on three claims:

1. HuskyAdvisor helps UWB students connect majors, courses, careers, and internships.
2. AI is embedded in scoring, LLM personalization, Crawl4AI ingestion, and retrieval readiness.
3. The team validates the system with tests, simulation reports, and honest scope boundaries.

## Criterion-to-File Map

| Rubric criterion | Evidence a grader can inspect |
| --- | --- |
| UW community impact | `web/src/pages/LandingPage.tsx` hero/problem/help sections, `README.md`, `docs/final_project_spec.md` |
| Public repository and deployment | `README.md` public links, `.github/workflows/deploy-web.yml`, `vercel.json`, `docs/deployment_and_public_access.md` |
| AI embedded meaningfully | `src/huskyadvisor/advisor.py` scoring logic, `api/llm.py` Groq/Llama enhancement, `src/huskyadvisor/crawl4ai_pipeline.py`, `web/src/pages/Recommendations.tsx` AI summary and trace |
| Not just a chat on the side | Profile submission calls `api/routers/profile.py`, which invokes `HuskyAdvisorEngine` and returns ranked results with `ai_trace` |
| Technical execution | `web/`, `api/`, `src/huskyadvisor/`, `tests/`, `scripts/run_deep_qa.py` |
| Stability and testing | `python3 -m unittest discover`, `npm run build`, `docs/deep_qa_500_scenario_report.md` |
| Project web presence | `web/src/pages/LandingPage.tsx` problem, user guide, architecture flow, tech stack, and live stat block |
| Milestones and planning | `docs/milestone_roadmap.md`, `CHANGELOG.md`, `docs/demo_readiness_checklist.md` |
| Peer contribution evidence | `docs/matiyas_role_summary.md`, `docs/matiyas_weekly_contribution_log.md`, commit history |
