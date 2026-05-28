from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel, Field

import api  # noqa: F401 — ensures sys.path is set before huskyadvisor imports
from huskyadvisor.models import AdvisingResult, StudentProfile

from api.engine import get_engine
from api.llm import enhance

router = APIRouter(prefix="/api/profile", tags=["profile"])
logger = logging.getLogger(__name__)


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


async def _safe_result(label: str, handler: Callable[[], Awaitable[AdvisingResult]]) -> AdvisingResult:
    try:
        return await handler()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("HuskyAdvisor API route failed: %s", label)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "huskyadvisor_route_failed",
                "route": label,
                "message": "The advising engine could not complete this request. Try again or use the demo-safe fallback.",
            },
        ) from exc


@router.post("/recommendations", response_model=AdvisingResult)
async def course_recommendations(req: ProfileRequest) -> AdvisingResult:
    async def handle() -> AdvisingResult:
        profile = _to_profile(req)
        target = profile.target_companies[0] if profile.target_companies else None
        result = get_engine().recommend_electives(profile, target)
        return await enhance(profile, result, "course")

    return await _safe_result("recommendations", handle)


@router.post("/companies", response_model=AdvisingResult)
async def company_alignment(req: ProfileRequest) -> AdvisingResult:
    async def handle() -> AdvisingResult:
        profile = _to_profile(req)
        result = get_engine().recommend_companies(profile)
        return await enhance(profile, result, "company alignment")

    return await _safe_result("companies", handle)


@router.post("/internship-prep", response_model=AdvisingResult)
async def internship_prep(req: ProfileRequest) -> AdvisingResult:
    async def handle() -> AdvisingResult:
        profile = _to_profile(req)
        result = get_engine().recommend_internship_prep(profile)
        return await enhance(profile, result, "internship preparation")

    return await _safe_result("internship-prep", handle)


@router.post("/roadmap", response_model=AdvisingResult)
async def quarter_roadmap(req: ProfileRequest) -> AdvisingResult:
    async def handle() -> AdvisingResult:
        profile = _to_profile(req)
        result = get_engine().build_quarter_plan(profile)
        return await enhance(profile, result, "quarter roadmap")

    return await _safe_result("roadmap", handle)


@router.post("/major", response_model=AdvisingResult)
async def major_suggestion(req: ProfileRequest) -> AdvisingResult:
    async def handle() -> AdvisingResult:
        profile = _to_profile(req)
        result = get_engine().suggest_major(req.interests or req.career_goals)
        return await enhance(profile, result, "major suggestion")

    return await _safe_result("major", handle)
