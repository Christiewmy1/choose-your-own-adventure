# HuskyAdvisor Team Dependency Tracker

## Purpose

This document makes cross-team dependencies visible so each person knows what they are waiting on and what they owe to others.

## Matiyas -> Frontend Team

Delivered:
- project website copy
- frontend handoff requirements
- website testing checklist
- sample personas
- persona-based expected results

Files:
- `docs/website_copy_blocks.md`
- `docs/frontend_handoff.md`
- `docs/website_testing_checklist.md`
- `data/sample_student_personas.json`
- `docs/persona_test_matrix.md`

Frontend team now needs to:
- replace placeholder site text with HuskyAdvisor copy
- replace generic example recommendations with HuskyAdvisor-aligned examples
- use the persona flow as part of demo and testing

## Matiyas -> Backend Team

Delivered:
- expanded course dataset
- local company dataset
- company-course mapping
- internship-prep playbooks
- source and evaluation documentation

Files:
- `data/uwb_courses_sample.json`
- `data/local_tech_companies.json`
- `data/company_course_mapping.json`
- `data/internship_prep_playbooks.json`
- `docs/source_reference_index.md`
- `docs/manual_evaluation_report.md`

Backend team now needs to:
- expose recommendation outputs in a frontend-friendly format
- ensure persona test cases produce believable results
- connect company alignment and internship-prep logic to the web flow

## Frontend -> Matiyas

Needed from frontend:
- actual implemented page structure
- screenshots of real pages
- final wording adjustments based on layout constraints

Once provided, Matiyas can:
- refine copy
- update project website documentation
- evaluate whether the live website matches project scope

## Backend -> Matiyas

Needed from backend:
- stable response format
- sample outputs for each website flow
- any changes to supported profile fields

Once provided, Matiyas can:
- update test matrix expectations
- improve the evaluation report
- tighten frontend/back-end alignment docs

## Shared Team Risks

- website and backend may drift apart if placeholder content remains in the UI
- project scope may drift if the team starts talking about live internships as if they are already implemented
- CSSE may look much stronger than Applied Computing or EE if the remaining data gaps are not addressed

## Immediate Accountability Summary

- Matiyas has already prepared content, data, source notes, and testing scaffolds
- Frontend now needs to implement the content and remove placeholders
- Backend now needs to support consistent outputs for the website flows
