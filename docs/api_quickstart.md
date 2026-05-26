# HuskyAdvisor API Quickstart

## Purpose

This document explains how to run the first local API version of HuskyAdvisor once dependencies are installed.

## Start The API

From the project root:

```bash
cd /Users/matiyasdawit/Desktop/CSS_382_Sp_26/AI_Project
PYTHONPATH=src uvicorn huskyadvisor.api_app:app --host 127.0.0.1 --port 8010
```

## Verify It Started

Open:

- `http://127.0.0.1:8010/health`
- `http://127.0.0.1:8010/docs`

The first should return a small health response. The second should open the FastAPI Swagger UI.

## Main Endpoints

- `POST /api/profile/recommendations`
- `POST /api/profile/companies`
- `POST /api/profile/internship-prep`
- `POST /api/profile/roadmap`
- `POST /api/major/suggest`

## Example Request Body

```json
{
  "major": "CSSE",
  "class_standing": "Junior",
  "completed_courses": ["CSS 142", "CSS 143", "CSS 342", "CSS 360"],
  "career_goals": ["systems", "embedded", "software engineering"],
  "target_companies": ["Boeing"]
}
```

## Why This Matters

This API is the bridge between the current HuskyAdvisor Python prototype and the future website. Once the frontend sends profile data here, it can render real recommendations instead of placeholder text.
