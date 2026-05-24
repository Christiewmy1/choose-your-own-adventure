# HuskyAdvisor API Contract Draft

## Purpose

This document defines the minimum backend responses the website should eventually consume. It keeps the frontend and backend aligned around the same data shape, even before the live API is fully implemented.

## Base Concept

Each HuskyAdvisor workflow should return a structured response with:
- `title`
- `summary`
- `recommendations`
- `evidence`
- `cautions`

This matches the current Python-side `AdvisingResult` structure and makes it easier for the frontend to render different pages consistently.

## Suggested Endpoints

### `POST /api/profile/recommendations`

**Purpose:**  
Return course recommendations for a student profile.

**Request body example:**

```json
{
  "major": "CSSE",
  "class_standing": "Junior",
  "completed_courses": ["CSS 142", "CSS 143", "CSS 342", "CSS 360"],
  "career_goals": ["systems", "embedded", "software engineering"],
  "target_companies": ["Boeing"]
}
```

**Response shape:**

```json
{
  "title": "Recommended 400-Level Electives",
  "summary": "For a Junior CSSE student targeting Boeing, these courses best match systems, aerospace, and reliable software preparation.",
  "recommendations": [
    "CSS 430 Operating Systems: ...",
    "CSS 422 Hardware and Computer Organization: ...",
    "CSS 458 Software Testing and Quality Assurance: ..."
  ],
  "evidence": [
    "CSS 430 overlaps with Boeing skills: systems, reliability.",
    "Your completed courses suggest you are reasonably prepared."
  ],
  "cautions": [
    "Check prerequisites for CSS 430: CSS 342 and CSS 360."
  ]
}
```

### `POST /api/profile/companies`

**Purpose:**  
Return local company alignment suggestions for a student profile.

**Response shape:**

```json
{
  "title": "Local Company Alignment",
  "summary": "These companies best match your current academic path and stated goals.",
  "recommendations": [
    "Boeing (Seattle area): focus on aerospace, embedded systems, large-scale engineering software.",
    "Microsoft Redmond (Redmond): focus on platform engineering, developer tools, cloud services, AI."
  ],
  "evidence": [
    "Boeing matches your goals through skills like systems and embedded."
  ],
  "cautions": [
    "These are company-alignment suggestions, not live job postings."
  ]
}
```

### `POST /api/profile/internship-prep`

**Purpose:**  
Return internship-preparation next steps.

**Response shape:**

```json
{
  "title": "Internship Prep Plan",
  "summary": "This plan suggests courses, project ideas, and skills that fit one likely internship pathway.",
  "recommendations": [
    "Recommended courses: CSS 430, CSS 458",
    "Build a systems-oriented project with testing."
  ],
  "evidence": [
    "Target companies in this playbook: Boeing, Microsoft Redmond.",
    "Suggested skills: systems, testing, reliability."
  ],
  "cautions": [
    "This is a preparation guide, not a live internship feed."
  ]
}
```

### `POST /api/profile/roadmap`

**Purpose:**  
Return a quarter-by-quarter roadmap for the student profile.

**Response shape:**

```json
{
  "title": "Quarter-by-Quarter Success Roadmap",
  "summary": "This roadmap matches one of HuskyAdvisor's structured preparation tracks.",
  "recommendations": [
    "Quarter 1: Strengthen core systems foundations. Suggested courses: CSS 430, CSS 458. Project goal: Build a small systems-oriented project with automated tests and clear documentation.",
    "Quarter 2: Expand distributed and production-ready thinking. Suggested courses: CSS 432, CSS 436. Project goal: Create a multi-component service or networking project."
  ],
  "evidence": [
    "This roadmap was selected because your goals overlap with the systems_software track.",
    "Target companies in this track: Boeing, Amazon Bellevue, Microsoft Redmond."
  ],
  "cautions": [
    "Confirm prerequisite sequencing with an advisor before treating this as an official degree plan."
  ]
}
```

## Frontend Rendering Notes

- `title` should become the page or section heading
- `summary` should appear near the top in short prose
- `recommendations` should render as the main list
- `evidence` should render as “Why these suggestions”
- `cautions` should render in a visually distinct note box

## MVP Implementation Note

The first live API does not need authentication or persistence. It only needs to accept a profile payload and return structured JSON that mirrors the current local HuskyAdvisor outputs.
