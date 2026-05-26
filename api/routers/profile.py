from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

import api  # noqa: F401 — ensures sys.path is set before huskyadvisor imports
from huskyadvisor.models import AdvisingResult, StudentProfile

from api.engine import get_engine
from api.llm import enhance

router = APIRouter(prefix="/api/profile", tags=["profile"])


class ProfileRequest(BaseModel):
    major: str
    class_standing: str
    completed_courses: list[str] = Field(default_factory=list)
    career_goals: list[str] = Field(default_factory=list)
    target_companies: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)


def _to_profile(req: ProfileRequest) -> StudentProfile:
    return StudentProfile(
        student_id="api-user",
        name="API User",
        campus="UW Bothell",
        major=req.major,
        class_standing=req.class_standing,
        gpa=3.0,
        completed_credits=90,
        completed_courses=req.completed_courses,
        preferred_learning_style="project-based",
        career_goals=req.career_goals or req.interests,
        target_companies=req.target_companies,
        internship_timeline="next summer",
    )


@router.post("/recommendations", response_model=AdvisingResult)
def course_recommendations(req: ProfileRequest) -> AdvisingResult:
    profile = _to_profile(req)
    target = profile.target_companies[0] if profile.target_companies else None
    result = get_engine().recommend_electives(profile, target)
    return enhance(profile, result, "course")


@router.post("/companies", response_model=AdvisingResult)
def company_alignment(req: ProfileRequest) -> AdvisingResult:
    profile = _to_profile(req)
    result = get_engine().recommend_companies(profile)
    return enhance(profile, result, "company alignment")


@router.post("/internship-prep", response_model=AdvisingResult)
def internship_prep(req: ProfileRequest) -> AdvisingResult:
    profile = _to_profile(req)
    result = get_engine().recommend_internship_prep(profile)
    return enhance(profile, result, "internship preparation")


@router.post("/roadmap", response_model=AdvisingResult)
def quarter_roadmap(req: ProfileRequest) -> AdvisingResult:
    profile = _to_profile(req)
    result = get_engine().build_quarter_plan(profile)
    return enhance(profile, result, "quarter roadmap")


@router.post("/major", response_model=AdvisingResult)
def major_suggestion(req: ProfileRequest) -> AdvisingResult:
    profile = _to_profile(req)
    result = get_engine().suggest_major(req.interests or req.career_goals)
    return enhance(profile, result, "major suggestion")
