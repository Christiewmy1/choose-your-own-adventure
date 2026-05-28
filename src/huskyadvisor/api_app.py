from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from huskyadvisor.api_models import MajorSuggestionRequest, ProfileRequest
from huskyadvisor.models import AdvisingResult, StudentProfile
from huskyadvisor.service import build_json_advisor


app = FastAPI(
    title="HuskyAdvisor API",
    version="0.1.0",
    description="Prototype API for UW Bothell-focused advising recommendations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:3001",
        "http://localhost:3001",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_student_profile(request: ProfileRequest) -> StudentProfile:
    return StudentProfile(
        student_id=request.student_id,
        name=request.name,
        campus=request.campus,
        major=request.major,
        class_standing=request.class_standing,
        gpa=request.gpa,
        completed_credits=request.completed_credits,
        completed_courses=request.completed_courses,
        preferred_learning_style=request.preferred_learning_style,
        career_goals=request.career_goals,
        target_companies=request.target_companies,
        internship_timeline=request.internship_timeline,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# api requests
@app.post("/api/profile/recommendations", response_model=AdvisingResult)
def profile_recommendations(request: ProfileRequest) -> AdvisingResult:
    advisor = build_json_advisor()
    profile = _build_student_profile(request)
    target_company = profile.target_companies[0] if profile.target_companies else None
    return advisor.recommend_electives(profile, target_company)


@app.post("/api/profile/companies", response_model=AdvisingResult)
def profile_companies(request: ProfileRequest) -> AdvisingResult:
    advisor = build_json_advisor()
    profile = _build_student_profile(request)
    return advisor.recommend_companies(profile)


@app.post("/api/profile/internship-prep", response_model=AdvisingResult)
def profile_internship_prep(request: ProfileRequest) -> AdvisingResult:
    advisor = build_json_advisor()
    profile = _build_student_profile(request)
    return advisor.recommend_internship_prep(profile)


@app.post("/api/profile/roadmap", response_model=AdvisingResult)
def profile_roadmap(request: ProfileRequest) -> AdvisingResult:
    advisor = build_json_advisor()
    profile = _build_student_profile(request)
    return advisor.build_quarter_plan(profile)


@app.post("/api/major/suggest", response_model=AdvisingResult)
def major_suggest(request: MajorSuggestionRequest) -> AdvisingResult:
    advisor = build_json_advisor()
    return advisor.suggest_major(request.interests)
