# HuskyAdvisor Demo Readiness Checklist

## Purpose

This checklist is for the team to confirm the project is truly demo-ready before presenting.

## Website

- [x] Landing page loads locally
- [x] Profile form loads
- [x] Results page renders without placeholder INFO/BUS content
- [x] Website clearly says UWB or UW Bothell
- [x] If the backend is unreachable, the website shows a clearly labeled demo-safe fallback instead of a dead result screen

## Backend

- [x] API starts locally
- [x] `/health` responds correctly
- [x] profile recommendations endpoint works
- [x] company alignment endpoint works
- [x] internship prep endpoint works
- [x] roadmap endpoint works
- [x] API contract tests cover the public result shape

## Advising Quality

- [x] Completed courses are not recommended again
- [x] Company suggestions look believable
- [x] Internship prep output includes remaining next steps
- [x] Roadmap output looks tied to the student profile

## Data Credibility

- [x] Course records and organized course groups exist for the currently supported UWB majors
- [x] Source notes exist for important course records
- [x] Official schedule snapshot is present
- [x] Multi-quarter schedule snapshot is present
- [x] Crawl4AI raw data, normalized data, and target manifests are separated

## Presentation Readiness

- [x] Team can explain what HuskyAdvisor is in one sentence
- [x] Team can explain what is built vs future scope
- [x] One persona-based example is ready for live demo
- [x] Slides match the actual project status

## Demo URLs

- Public website: `https://christiewmy1.github.io/choose-your-own-adventure/`
- API health check: `https://huskyadvisor-api-matiyas.vercel.app/health`
- API base URL: `https://huskyadvisor-api-matiyas.vercel.app`

## Final Deployment Freshness Check

- [x] Local recommendation engine passes the 560-profile deep QA simulation.
- [x] Local API contract includes `ai_trace`.
- [x] Public backend health endpoint responds.
- [x] Public backend has redeployed the newest branch data/code.

Current note: the refreshed public backend at `https://huskyadvisor-api-matiyas.vercel.app` exposes the `ai_trace_v1` contract, reports 140 company records, and recognizes `JPMorgan Chase Technology` in profile recommendations.

## Best Live Demo Profile

- Major: `Computer Science and Software Engineering`
- Standing: `Junior`
- Completed courses: `CSS 142, CSS 143, CSS 301`
- Career goals: `cloud, software engineering`
- Target company: `Microsoft Redmond`
