# HuskyAdvisor Frontend Handoff

## Purpose

This document turns the current HuskyAdvisor MVP into frontend-ready requirements. It is meant to help the website team connect the actual project logic to the pages a student will use.

## Core Pages

### 1. Landing Page

**Goal:**  
Explain what HuskyAdvisor is and why a UWB student would use it.

**Must include:**

- project title and short tagline
- short problem statement
- one or two example questions
- a clear “Start” button

**Copy source:**  
`docs/project_website_content.md`

### 2. Profile Input Page

**Goal:**  
Collect the minimum information needed for personalized recommendations.

**Fields to include:**

- major
- class standing
- completed courses
- career goals
- target company or target field

### 3. Recommendation Results Page

**Goal:**  
Show course recommendations clearly and explain why they were chosen.

**Must include:**

- top course recommendations
- short explanation for each
- prerequisite reminders
- note that this is planning support, not official degree approval

**Backend-aligned mode:**  
`profile-demo`

### 4. Company Alignment Section

**Goal:**  
Connect a student’s path to local employers in a believable way.

**Must include:**

- 2–3 suggested companies
- why those companies fit
- which courses connect to those companies
- note that this is not a live job board

**Backend-aligned mode:**  
`company-demo`

### 5. Internship Prep Section

**Goal:**  
Translate recommendations into concrete next steps.

**Must include:**

- recommended courses
- project ideas
- suggested skills
- target companies or pathway

**Backend-aligned mode:**  
`internship-demo`

## MVP User Flow

1. Student opens the landing page
2. Student clicks “Start”
3. Student fills out a short profile
4. Student sees recommended courses
5. Student can explore company alignment and internship prep

## Important Frontend Notes

- Keep the first version simple and readable
- Prioritize HuskyAdvisor-specific content over generic placeholder examples
- Try to replace unrelated `INFO` or generic business examples with the real UWB-style course/company content from the datasets

## Highest-Value Frontend Improvement

If the frontend team does only one thing first, it should be:

**Replace placeholder recommendations with real HuskyAdvisor-aligned outputs and language.**
