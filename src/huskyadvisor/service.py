from __future__ import annotations

from huskyadvisor.advisor import HuskyAdvisorEngine
from huskyadvisor.json_data import (
    load_company_course_mapping,
    load_company_intent_profiles,
    load_company_records,
    load_course_records,
    load_internship_playbooks,
    load_major_records,
    load_quarter_plan_templates,
    load_recent_offering_terms,
)


def build_json_advisor() -> HuskyAdvisorEngine:
    return HuskyAdvisorEngine(
        load_major_records(),
        load_course_records(),
        load_company_records(),
        recent_offerings=load_recent_offering_terms(),
        company_course_mapping=load_company_course_mapping(),
        company_intent_profiles=load_company_intent_profiles(),
        internship_playbooks=load_internship_playbooks(),
        quarter_plan_templates=load_quarter_plan_templates(),
    )
