# Milestone Roadmap

## Milestone 1: Problem framing and proposal

Goals:

- define the UWB community problem
- choose the initial advising scope
- outline the AI/recommendation strategy
- set up repository access and team roles

Outputs:

- technical design draft
- system overview
- initial project website content draft

## Milestone 2: MVP recommendation engine

Goals:

- create a working local recommendation engine
- load initial course and company datasets
- support basic student-profile-driven recommendations

Outputs:

- `src/huskyadvisor/advisor.py`
- `src/huskyadvisor/json_data.py`
- sample datasets in `data/`

## Milestone 3: Website and API integration

Goals:

- add a React frontend
- expose the recommendation engine through FastAPI
- connect the frontend to the backend

Outputs:

- `web/`
- `api/`
- public website deployment workflow

## Milestone 4: Evaluation and expansion

Goals:

- expand majors, courses, companies, and company mappings
- improve completed-course filtering
- improve roadmap and internship-prep realism
- add regression testing and simulated profile evaluation

Outputs:

- major pathway expansion
- company dataset expansion
- simulation reports
- regression tests

## Milestone 5: Final polish

Goals:

- clean the repo and documentation
- align README, architecture docs, and deployment notes
- improve rubric-facing clarity
- strengthen demo readiness

Outputs:

- updated README
- deployment guide
- AI integration strategy doc
- rubric alignment audit

## Remaining final-mile tasks

- confirm the public API is reachable from the live site without manual local setup
- tighten newer major pathways with deeper metadata
- verify the public site after final deployment refresh
