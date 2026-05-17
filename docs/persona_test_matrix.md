# HuskyAdvisor Persona Test Matrix

## Purpose

This document connects sample student personas to expected HuskyAdvisor behavior. It gives the team a concrete way to test whether the frontend and backend are showing believable results.

## Persona 1: Junior CSSE Student Targeting Boeing

**Persona source:**  
`data/sample_student_personas.json` -> `junior_csse_boeing`

**Expected course themes:**
- operating systems
- hardware/computer organization
- testing or quality assurance

**Expected company behavior:**
- Boeing should appear high in the alignment list
- company reasoning should mention systems, embedded, or aerospace-relevant work

**Expected internship-prep behavior:**
- should recommend projects tied to systems or embedded work
- should suggest strengthening hardware-aware software skills

## Persona 2: Sophomore Applied Computing Student Interested in Cloud

**Persona source:**  
`data/sample_student_personas.json` -> `sophomore_app_cloud`

**Expected course themes:**
- databases
- web programming
- cloud or service-oriented systems

**Expected company behavior:**
- Microsoft or Amazon should appear as reasonable matches
- reasoning should mention cloud, platform, or scalable systems

**Expected internship-prep behavior:**
- should suggest building a small web/cloud project
- should highlight portfolio-building and backend skill growth

## Persona 3: Junior EE Student Interested in Embedded Systems

**Persona source:**  
`data/sample_student_personas.json` -> `junior_ee_embedded`

**Expected course themes:**
- embedded systems
- hardware/software integration
- low-level systems or design

**Expected company behavior:**
- T-Mobile, Boeing, or another systems-oriented company should be plausible
- explanation should mention firmware, devices, or communication systems

**Expected internship-prep behavior:**
- should suggest an embedded or hardware project
- should highlight practical implementation skills

## Persona 4: Senior CSSE Student Interested in Quality and Reliability

**Persona source:**  
`data/sample_student_personas.json` -> `senior_csse_quality`

**Expected course themes:**
- software testing
- backend systems
- reliability or production-readiness work

**Expected company behavior:**
- Amazon or Microsoft should be reasonable alignments
- explanation should mention scale, quality, or backend systems

**Expected internship-prep behavior:**
- should focus on testing discipline, system reliability, and portfolio polish

## How To Use This

1. Load one persona into the profile flow
2. Run the relevant HuskyAdvisor output
3. Compare the actual result to the expected themes above
4. Record mismatches in `docs/manual_evaluation_report.md`
