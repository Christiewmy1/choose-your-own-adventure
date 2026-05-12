from __future__ import annotations

from huskyadvisor.models import (
    CompanyRecord,
    CourseRecord,
    MajorRecord,
    ProfessorRecord,
    StudentProfile,
)


SAMPLE_STUDENT = StudentProfile(
    student_id="uwb-001",
    name="Sample Student",
    major="CSSE",
    class_standing="Junior",
    gpa=3.42,
    completed_credits=105,
    completed_courses=["CSS 342", "CSS 360", "CSS 370"],
    preferred_learning_style="structured, project-based",
    career_goals=["software engineering", "aerospace systems"],
    target_companies=["Boeing"],
    internship_timeline="next summer",
)


SAMPLE_COURSES = [
    CourseRecord(
        course_code="CSS 422",
        title="Hardware and Computer Organization",
        level=400,
        department="CSS",
        description=(
            "Explores lower-level machine organization, performance tradeoffs, and system "
            "interfaces relevant to hardware-software collaboration."
        ),
        major_tags=["CSSE", "EE"],
        career_tags=["embedded", "aerospace", "performance", "systems"],
        prerequisite_text="CSS 342",
        project_emphasis="medium",
    ),
    CourseRecord(
        course_code="CSS 430",
        title="Operating Systems",
        level=400,
        department="CSS",
        description=(
            "Focuses on processes, threads, scheduling, memory management, and systems "
            "programming. Strong fit for students interested in reliable large-scale software."
        ),
        major_tags=["CSSE"],
        career_tags=["systems", "backend", "aerospace", "embedded"],
        prerequisite_text="CSS 342 and CSS 360",
        project_emphasis="medium-high",
    ),
    CourseRecord(
        course_code="CSS 432",
        title="Networking and Distributed Systems",
        level=400,
        department="CSS",
        description=(
            "Covers networking fundamentals and distributed-system design. Helpful for "
            "mission-critical and connected software systems."
        ),
        major_tags=["CSSE"],
        career_tags=["systems", "networking", "backend", "aerospace"],
        prerequisite_text="CSS 360",
        project_emphasis="medium-high",
    ),
    CourseRecord(
        course_code="CSS 436",
        title="Cloud Computing",
        level=400,
        department="CSS",
        description=(
            "Introduces distributed services, cloud deployment, and scalable architectures "
            "useful for enterprise software environments."
        ),
        major_tags=["CSSE", "Applied Computing"],
        career_tags=["cloud", "backend", "devops"],
        prerequisite_text="CSS 360",
        project_emphasis="high",
    ),
    CourseRecord(
        course_code="CSS 458",
        title="Software Testing and Quality Assurance",
        level=400,
        department="CSS",
        description=(
            "Focuses on verification, validation, and dependable software development "
            "practices for production-grade systems."
        ),
        major_tags=["CSSE", "Applied Computing"],
        career_tags=["testing", "reliability", "backend", "aerospace"],
        prerequisite_text="CSS 360",
        project_emphasis="medium",
    ),
    CourseRecord(
        course_code="EE 450",
        title="Embedded Systems Design",
        level=400,
        department="EE",
        description=(
            "Covers microcontrollers, hardware-software integration, and real-world system "
            "constraints common in embedded engineering."
        ),
        major_tags=["EE", "CSSE"],
        career_tags=["embedded", "aerospace", "hardware", "systems"],
        prerequisite_text="Instructor or department prerequisites vary",
        project_emphasis="high",
    ),
]


SAMPLE_MAJORS = [
    MajorRecord(
        major_name="CSSE",
        degree_type="B.S.",
        summary="Best fit for students who want strong software engineering depth and project-heavy computing work.",
        best_for=["software engineering", "systems", "backend", "technical project work"],
        typical_courses=["CSS 342", "CSS 360", "CSS 430", "CSS 458"],
        career_paths=["software engineer", "systems engineer", "backend developer"],
    ),
    MajorRecord(
        major_name="Applied Computing",
        degree_type="B.A.",
        summary="Best fit for students who want flexible computing skills with applied problem-solving across domains.",
        best_for=["product work", "data-informed applications", "IT", "cross-functional roles"],
        typical_courses=["CSS 301", "CSS 436", "BIS 360"],
        career_paths=["application developer", "technical analyst", "IT systems role"],
    ),
    MajorRecord(
        major_name="Electrical Engineering",
        degree_type="B.S.",
        summary="Best fit for students interested in hardware, circuits, embedded systems, and device-level engineering.",
        best_for=["embedded systems", "hardware", "robotics", "signal and device work"],
        typical_courses=["EE 271", "EE 331", "EE 450"],
        career_paths=["embedded engineer", "hardware engineer", "systems integration engineer"],
    ),
]


SAMPLE_PROFESSORS = [
    ProfessorRecord(
        professor_id="prof-001",
        name="Dr. Avery Chen",
        department="CSS",
        teaching_style_tags=["structured", "project-based", "clear lectures"],
        sentiment_summary="Often described as organized and practical with fair project expectations.",
        source_confidence="low-medium",
    ),
    ProfessorRecord(
        professor_id="prof-002",
        name="Dr. Maya Patel",
        department="CSS",
        teaching_style_tags=["fast-paced", "theory-heavy", "rigorous"],
        sentiment_summary="Strong for motivated students who want deeper technical challenge.",
        source_confidence="low-medium",
    ),
]


SAMPLE_COMPANIES = [
    CompanyRecord(
        company_id="company-001",
        name="Boeing",
        city="Seattle area",
        domain_focus="aerospace, embedded systems, large-scale engineering software",
        hiring_seasons=["fall", "winter"],
        target_skills=["systems", "C++", "reliability", "embedded", "testing"],
        notes="Good target for students interested in aerospace software and systems engineering.",
    ),
    CompanyRecord(
        company_id="company-002",
        name="Google Kirkland",
        city="Kirkland",
        domain_focus="distributed systems, cloud, infrastructure",
        hiring_seasons=["late summer", "fall"],
        target_skills=["algorithms", "distributed systems", "backend", "cloud"],
        notes="Useful benchmark for scalable systems and infrastructure-oriented preparation.",
    ),
    CompanyRecord(
        company_id="company-003",
        name="T-Mobile",
        city="Bellevue",
        domain_focus="telecom platforms, cloud systems, large-scale applications",
        hiring_seasons=["fall", "spring"],
        target_skills=["networking", "backend", "cloud", "reliability"],
        notes="Relevant for networked systems and production software roles in the region.",
    ),
]
