from __future__ import annotations

import api  # noqa: F401 — triggers sys.path setup in api/__init__.py

from huskyadvisor.advisor import HuskyAdvisorEngine
from huskyadvisor.json_data import (
    load_company_course_mapping,
    load_company_records,
    load_course_records,
    load_internship_playbooks,
    load_quarter_plan_templates,
    load_recent_offering_terms,
)
from huskyadvisor.sample_data import SAMPLE_MAJORS

_engine: HuskyAdvisorEngine | None = None


def get_engine() -> HuskyAdvisorEngine:
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine


def _build_engine() -> HuskyAdvisorEngine:
    return HuskyAdvisorEngine(
        majors=SAMPLE_MAJORS,
        courses=load_course_records(),
        companies=load_company_records(),
        recent_offerings=load_recent_offering_terms(),
        company_course_mapping=load_company_course_mapping(),
        internship_playbooks=load_internship_playbooks(),
        quarter_plan_templates=load_quarter_plan_templates(),
    )
