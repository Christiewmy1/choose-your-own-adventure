from __future__ import annotations

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI


def build_self_query_retriever(vector_store: Chroma) -> SelfQueryRetriever:
    metadata_field_info = [
        AttributeInfo(
            name="entity_type",
            description="Type of record such as course, professor, or company",
            type="string",
        ),
        AttributeInfo(
            name="course_level",
            description="Numeric course level, such as 400 for senior electives",
            type="integer",
        ),
        AttributeInfo(
            name="major_tags",
            description="Majors associated with a course, such as CSSE or EE",
            type="string",
        ),
        AttributeInfo(
            name="career_tags",
            description="Career or skill alignment such as aerospace, systems, backend, or cloud",
            type="string",
        ),
        AttributeInfo(
            name="company_name",
            description="Name of a local company related to the student's goals",
            type="string",
        ),
    ]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vector_store,
        document_contents="UWB advising records about courses, professors, and local tech companies",
        metadata_field_info=metadata_field_info,
        enable_limit=True,
        search_kwargs={"k": 6},
    )
