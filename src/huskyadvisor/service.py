from __future__ import annotations

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


def build_json_advisor() -> HuskyAdvisorEngine:
    return HuskyAdvisorEngine(
        SAMPLE_MAJORS,
        load_course_records(),
        load_company_records(),
        recent_offerings=load_recent_offering_terms(),
        company_course_mapping=load_company_course_mapping(),
        internship_playbooks=load_internship_playbooks(),
        quarter_plan_templates=load_quarter_plan_templates(),
    )
