from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    major: str
    class_standing: str
    completed_courses: List[str] = Field(default_factory=list)
    career_goals: List[str] = Field(default_factory=list)
    target_companies: List[str] = Field(default_factory=list)
    gpa: float = 3.3
    completed_credits: int = 90
    preferred_learning_style: str = "project-based"
    internship_timeline: str = "next summer"
    campus: str = "UW Bothell"
    name: str = "Website Demo Student"
    student_id: str = "web-profile"


class MajorSuggestionRequest(BaseModel):
    interests: List[str] = Field(default_factory=list)
