from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    student_id: str
    name: str
    campus: str = "UW Bothell"
    major: str
    class_standing: str
    gpa: float
    completed_credits: int
    completed_courses: List[str] = Field(default_factory=list)
    preferred_learning_style: str
    career_goals: List[str] = Field(default_factory=list)
    target_companies: List[str] = Field(default_factory=list)
    internship_timeline: str


class CourseRecord(BaseModel):
    course_code: str
    title: str
    level: int
    department: str
    description: str
    major_tags: List[str] = Field(default_factory=list)
    career_tags: List[str] = Field(default_factory=list)
    prerequisite_text: str
    project_emphasis: str
    source_type: str = "unknown"
    source_confidence: str = "medium"
    source_url: str | None = None


class MajorRecord(BaseModel):
    major_name: str
    degree_type: str
    summary: str
    best_for: List[str] = Field(default_factory=list)
    typical_courses: List[str] = Field(default_factory=list)
    career_paths: List[str] = Field(default_factory=list)
    aliases: List[str] = Field(default_factory=list)
    support_tier: str = "partial"
    support_scope_notes: str = ""
    course_groups: dict[str, List[str]] = Field(default_factory=dict)
    source_url: str | None = None


class ProfessorRecord(BaseModel):
    professor_id: str
    name: str
    department: str
    teaching_style_tags: List[str] = Field(default_factory=list)
    sentiment_summary: str
    source_confidence: str


class CompanyRecord(BaseModel):
    company_id: str
    name: str
    city: str
    domain_focus: str
    hiring_seasons: List[str] = Field(default_factory=list)
    target_skills: List[str] = Field(default_factory=list)
    notes: str


class AITrace(BaseModel):
    recommendation_engine: str = "profile-aware structured scoring"
    llm_enhancement: str = "not attempted"
    llm_model: str | None = None
    data_ingestion: str = "curated JSON datasets with Crawl4AI-ready refresh pipeline"
    retrieval_readiness: str = "normalized documents can feed optional retrieval/vector workflows"
    fallback_mode: bool = False
    decision_inputs: List[str] = Field(default_factory=list)


class AdvisingResult(BaseModel):
    title: str
    summary: str
    recommendations: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    cautions: List[str] = Field(default_factory=list)
    ai_trace: AITrace = Field(default_factory=AITrace)
