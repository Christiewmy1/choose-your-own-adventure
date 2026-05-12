from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from huskyadvisor.models import CompanyRecord, CourseRecord, ProfessorRecord


def _course_to_document(course: CourseRecord) -> Document:
    content = (
        f"{course.course_code}: {course.title}. "
        f"{course.description} "
        f"Prerequisites: {course.prerequisite_text}. "
        f"Project emphasis: {course.project_emphasis}."
    )
    return Document(
        page_content=content,
        metadata={
            "entity_type": "course",
            "course_code": course.course_code,
            "course_level": course.level,
            "department": course.department,
            "major_tags": ", ".join(course.major_tags),
            "career_tags": ", ".join(course.career_tags),
        },
    )


def _professor_to_document(professor: ProfessorRecord) -> Document:
    content = (
        f"{professor.name} in {professor.department}. "
        f"Teaching style tags: {', '.join(professor.teaching_style_tags)}. "
        f"Summary: {professor.sentiment_summary}."
    )
    return Document(
        page_content=content,
        metadata={
            "entity_type": "professor",
            "department": professor.department,
            "source_confidence": professor.source_confidence,
            "teaching_style_tags": ", ".join(professor.teaching_style_tags),
        },
    )


def _company_to_document(company: CompanyRecord) -> Document:
    content = (
        f"{company.name} in {company.city}. "
        f"Domain focus: {company.domain_focus}. "
        f"Hiring seasons: {', '.join(company.hiring_seasons)}. "
        f"Target skills: {', '.join(company.target_skills)}. "
        f"Notes: {company.notes}"
    )
    return Document(
        page_content=content,
        metadata={
            "entity_type": "company",
            "company_name": company.name,
            "city": company.city,
            "target_skills": ", ".join(company.target_skills),
        },
    )


def build_documents(
    courses: Iterable[CourseRecord],
    professors: Iterable[ProfessorRecord],
    companies: Iterable[CompanyRecord],
) -> List[Document]:
    documents: List[Document] = []
    documents.extend(_course_to_document(course) for course in courses)
    documents.extend(_professor_to_document(professor) for professor in professors)
    documents.extend(_company_to_document(company) for company in companies)
    return documents


def create_vector_store(documents: List[Document], persist_dir: str = ".chroma") -> Chroma:
    embeddings = OpenAIEmbeddings()
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(Path(persist_dir)),
        collection_name="huskyadvisor",
    )
