from __future__ import annotations

import argparse
import os

from huskyadvisor.advisor import HuskyAdvisorEngine
from huskyadvisor.formatter import format_result
from huskyadvisor.json_data import (
    load_company_course_mapping,
    load_company_records,
    load_course_records,
    load_internship_playbooks,
    load_recent_offering_terms,
    load_student_profile,
)
from huskyadvisor.sample_data import (
    SAMPLE_COMPANIES,
    SAMPLE_COURSES,
    SAMPLE_MAJORS,
    SAMPLE_PROFESSORS,
    SAMPLE_STUDENT,
)


def build_prompt(query: str, context: str) -> str:
    return f"""
You are HuskyAdvisor, a UWB-specific academic and career advising assistant.

Student profile:
- Campus: {SAMPLE_STUDENT.campus}
- Major: {SAMPLE_STUDENT.major}
- Standing: {SAMPLE_STUDENT.class_standing}
- GPA: {SAMPLE_STUDENT.gpa}
- Completed credits: {SAMPLE_STUDENT.completed_credits}
- Completed courses: {", ".join(SAMPLE_STUDENT.completed_courses)}
- Career goals: {", ".join(SAMPLE_STUDENT.career_goals)}
- Target companies: {", ".join(SAMPLE_STUDENT.target_companies)}
- Learning style: {SAMPLE_STUDENT.preferred_learning_style}

User question:
{query}

Retrieved context:
{context}

Instructions:
- Recommend the most relevant 400-level electives.
- Explain why each course matches Boeing-style work.
- Mention prerequisite or readiness considerations when relevant.
- Keep the answer grounded in the provided context.
""".strip()


def run_llm_query(query: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is required to run the LangChain prototype.")

    from langchain_openai import ChatOpenAI

    from huskyadvisor.retrieval import build_self_query_retriever
    from huskyadvisor.vector_store import build_documents, create_vector_store

    documents = build_documents(SAMPLE_COURSES, SAMPLE_PROFESSORS, SAMPLE_COMPANIES)
    vector_store = create_vector_store(documents)
    retriever = build_self_query_retriever(vector_store)
    retrieved_docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    response = llm.invoke(build_prompt(query, context))

    metadata_lines = [f"- {doc.metadata}" for doc in retrieved_docs]
    return "\n".join(
        [
            "Question:",
            query,
            "",
            "Retrieved documents:",
            *metadata_lines,
            "",
            "HuskyAdvisor response:",
            response.content,
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HuskyAdvisor MVP demo.")
    parser.add_argument(
        "--mode",
        choices=["electives", "major", "roadmap", "profile-demo", "company-demo", "internship-demo", "llm-demo"],
        default="electives",
        help="Which advising workflow to run.",
    )
    parser.add_argument(
        "--query",
        default="I'm a Junior CSSE student at UWB; which 400-level electives should I take if I want to work at Boeing?",
        help="Free-form question for the llm-demo mode.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    advisor = HuskyAdvisorEngine(SAMPLE_MAJORS, SAMPLE_COURSES, SAMPLE_COMPANIES)

    if args.mode == "electives":
        result = advisor.recommend_electives(SAMPLE_STUDENT, "Boeing")
        print(format_result(result))
        return

    if args.mode == "major":
        result = advisor.suggest_major(["software engineering", "systems", "project work"])
        print(format_result(result))
        return

    if args.mode == "roadmap":
        result = advisor.build_quarter_plan(SAMPLE_STUDENT)
        print(format_result(result))
        return

    if args.mode == "profile-demo":
        profile = load_student_profile()
        json_courses = load_course_records()
        json_companies = load_company_records()
        recent_offerings = load_recent_offering_terms()
        company_mapping = load_company_course_mapping()
        internship_playbooks = load_internship_playbooks()
        json_advisor = HuskyAdvisorEngine(
            SAMPLE_MAJORS,
            json_courses,
            json_companies,
            recent_offerings=recent_offerings,
            company_course_mapping=company_mapping,
            internship_playbooks=internship_playbooks,
        )
        result = json_advisor.recommend_electives(
            profile,
            profile.target_companies[0] if profile.target_companies else None,
        )
        print(format_result(result))
        return

    if args.mode == "company-demo":
        profile = load_student_profile()
        json_courses = load_course_records()
        json_companies = load_company_records()
        recent_offerings = load_recent_offering_terms()
        company_mapping = load_company_course_mapping()
        internship_playbooks = load_internship_playbooks()
        json_advisor = HuskyAdvisorEngine(
            SAMPLE_MAJORS,
            json_courses,
            json_companies,
            recent_offerings=recent_offerings,
            company_course_mapping=company_mapping,
            internship_playbooks=internship_playbooks,
        )
        result = json_advisor.recommend_companies(profile)
        print(format_result(result))
        return

    if args.mode == "internship-demo":
        profile = load_student_profile()
        json_courses = load_course_records()
        json_companies = load_company_records()
        recent_offerings = load_recent_offering_terms()
        company_mapping = load_company_course_mapping()
        internship_playbooks = load_internship_playbooks()
        json_advisor = HuskyAdvisorEngine(
            SAMPLE_MAJORS,
            json_courses,
            json_companies,
            recent_offerings=recent_offerings,
            company_course_mapping=company_mapping,
            internship_playbooks=internship_playbooks,
        )
        result = json_advisor.recommend_internship_prep(profile)
        print(format_result(result))
        return

    print(run_llm_query(args.query))


if __name__ == "__main__":
    main()
