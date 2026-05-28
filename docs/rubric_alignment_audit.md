# Rubric Alignment Audit

## Purpose

This document maps the current HuskyAdvisor repository to the DYOP project requirements and highlights what is strong, what is weak, and what still needs confirmation.

## 1. UW Community Impact

Status: **Strong**

Evidence:

- UWB-specific advising problem
- UWB-focused course and pathway data
- local company alignment for students
- public-facing explanation in `README.md` and website content docs

Main risk:

- impact is strongest for computing/engineering students, not the full UWB population

## 2. AI Integration

Status: **Moderate to strong**

Evidence:

- embedded recommendation scoring logic
- company-intent matching
- roadmap and internship-playbook selection
- optional retrieval modules using LangChain and Chroma

Main risk:

- the current deployed MVP uses the structured engine more than the retrieval/LLM path

## 3. Technical Execution

Status: **Moderate**

Evidence:

- React frontend
- FastAPI API
- structured datasets
- regression tests
- simulation coverage reports

Main risk:

- public deployment reliability must be verified end-to-end
- some pathways still have thinner metadata

## 4. Project Web Presence

Status: **Moderate to strong**

Evidence:

- public website exists
- README now explains project purpose, architecture, and deployment
- website copy blocks and testing docs exist

Main risk:

- the public website should still be manually checked after final deployment

## 5. Milestones and Planning

Status: **Moderate**

Evidence:

- technical design document
- milestone roadmap
- many iteration docs and evaluation docs
- simulation reports and testing artifacts

Main risk:

- the timeline is reconstructed from delivered artifacts more than from a single polished proposal PDF

## 6. Peer Review

Status: **Unverifiable from repo**

Evidence:

- cannot be confirmed from repository contents alone

Main risk:

- depends entirely on Canvas submission and teammate feedback

## Final honest assessment

The repository now presents a much stronger and more coherent story than before, but the final grade still depends heavily on one external confirmation:

- whether the public website and public API both work reliably during grading

That is the most important final verification step.
