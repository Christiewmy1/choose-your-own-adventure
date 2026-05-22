from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from huskyadvisor.models import CompanyRecord, CourseRecord, StudentProfile


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_COURSE_JSON = PROJECT_ROOT / "data" / "uwb_courses_sample.json"
DEFAULT_PROFILE_JSON = PROJECT_ROOT / "data" / "student_profile.json"
DEFAULT_COMPANY_JSON = PROJECT_ROOT / "data" / "local_tech_companies.json"
DEFAULT_RECENT_CATALOG_JSON = PROJECT_ROOT / "data" / "uwb_recent_css_catalog_summary.json"
DEFAULT_COMPANY_MAPPING_JSON = PROJECT_ROOT / "data" / "company_course_mapping.json"
DEFAULT_INTERNSHIP_PLAYBOOK_JSON = PROJECT_ROOT / "data" / "internship_prep_playbooks.json"
DEFAULT_QUARTER_PLAN_JSON = PROJECT_ROOT / "data" / "quarter_plan_templates.json"


def load_course_records(path: Path | None = None) -> list[CourseRecord]:
    source = path or DEFAULT_COURSE_JSON
    with source.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    records: list[CourseRecord] = []
    for item in payload.get("courses", []):
        code = _normalize_code(item.get("code", ""))
        department = item.get("department") or (code.split()[0] if code else "Unknown")
        level = int(item.get("level") or _parse_level(code))
        career_tags = item.get("career_tags") or _infer_career_tags(item.get("description", ""))
        major_tags = item.get("majors") or _infer_major_tags(code, department)
        records.append(
            CourseRecord(
                course_code=code,
                title=item.get("title", "Untitled Course"),
                level=level,
                department=department,
                description=item.get("description", ""),
                major_tags=major_tags,
                career_tags=career_tags,
                prerequisite_text=item.get("prerequisites", "See catalog"),
                project_emphasis=item.get("project_emphasis") or _infer_project_emphasis(item.get("description", "")),
                source_type=item.get("source_type", "unknown"),
                source_confidence=item.get("source_confidence", "medium"),
                source_url=item.get("source_url"),
            )
        )
    return records


def load_student_profile(path: Path | None = None) -> StudentProfile:
    source = path or DEFAULT_PROFILE_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)

    completed = [_normalize_code(code) for code in payload.get("completed_course_codes", [])]
    return StudentProfile(
        student_id="json-profile",
        name="Profile Demo Student",
        campus="UW Bothell",
        major=payload.get("major", "CSSE"),
        class_standing=payload.get("class_standing", "Junior"),
        gpa=float(payload.get("gpa", 3.3)),
        completed_credits=int(payload.get("completed_credits", 90)),
        completed_courses=completed,
        preferred_learning_style=payload.get("preferred_learning_style", "project-based"),
        career_goals=payload.get("career_goals", ["software engineering"]),
        target_companies=payload.get("target_companies", []),
        internship_timeline=payload.get("internship_timeline", "next summer"),
    )


def load_company_records(path: Path | None = None) -> list[CompanyRecord]:
    source = path or DEFAULT_COMPANY_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)

    records: list[CompanyRecord] = []
    for item in payload.get("companies", []):
        records.append(
            CompanyRecord(
                company_id=item["company_id"],
                name=item["name"],
                city=item["city"],
                domain_focus=item["domain_focus"],
                hiring_seasons=item.get("hiring_seasons", []),
                target_skills=item.get("target_skills", []),
                notes=item.get("notes", ""),
            )
        )
    return records


def load_recent_offering_terms(path: Path | None = None) -> dict[str, list[str]]:
    source = path or DEFAULT_RECENT_CATALOG_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)

    return {
        _normalize_code(item["course"]): item.get("recent_terms", [])
        for item in payload.get("courses", [])
    }


def load_company_course_mapping(path: Path | None = None) -> dict[str, list[str]]:
    source = path or DEFAULT_COMPANY_MAPPING_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)

    return {
        item["company"]: [_normalize_code(code) for code in item.get("recommended_courses", [])]
        for item in payload.get("mappings", [])
    }


def load_internship_playbooks(path: Path | None = None) -> list[dict[str, Any]]:
    source = path or DEFAULT_INTERNSHIP_PLAYBOOK_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)
    return payload.get("playbooks", [])


def load_quarter_plan_templates(path: Path | None = None) -> list[dict[str, Any]]:
    source = path or DEFAULT_QUARTER_PLAN_JSON
    with source.open(encoding="utf-8") as handle:
        payload: dict[str, Any] = json.load(handle)
    return payload.get("templates", [])


def _normalize_code(value: str) -> str:
    return " ".join(str(value).strip().upper().split())


def _parse_level(code: str) -> int:
    parts = code.split()
    for token in reversed(parts):
        if token.isdigit():
            return int(token[0]) * 100
    return 0


def _infer_major_tags(code: str, department: str) -> list[str]:
    normalized_department = department.upper()
    if code.startswith("EE ") or normalized_department == "EE":
        return ["EE", "CSSE"]
    if code.startswith("CSS "):
        return ["CSSE", "Applied Computing"]
    return ["Applied Computing"]


def _infer_career_tags(description: str) -> list[str]:
    desc = description.lower()
    tags: list[str] = []
    keyword_map = {
        "systems": ["operating system", "systems", "memory", "threads"],
        "backend": ["software", "distributed", "scalable"],
        "testing": ["testing", "validation", "verification"],
        "embedded": ["hardware", "microcontroller", "embedded"],
        "cloud": ["cloud", "distributed", "scalable"],
        "networking": ["network", "distributed-system"],
        "aerospace": ["reliable", "real-world system", "hardware-software"],
    }
    for tag, keywords in keyword_map.items():
        if any(keyword in desc for keyword in keywords):
            tags.append(tag)
    return tags or ["software engineering"]


def _infer_project_emphasis(description: str) -> str:
    desc = description.lower()
    if "project" in desc or "hands-on" in desc or "build" in desc:
        return "high"
    return "medium"
