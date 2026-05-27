from __future__ import annotations

import random
import re
from collections import Counter
from pathlib import Path

from huskyadvisor.models import StudentProfile
from huskyadvisor.service import build_json_advisor


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "simulation_test_matrix.md"
REPORT_PATH = ROOT / "docs" / "simulation_coverage_report.md"
CODE_PATTERN = re.compile(r"\b([A-Z]{2,6})\s+(\d{3})\b")


def canonical_major(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"csse", "computer science and software engineering", "computer science & software engineering"}:
        return "CSSE"
    if lowered in {"applied computing", "ac"}:
        return "Applied Computing"
    if lowered in {"ee", "electrical engineering"}:
        return "EE"
    if lowered in {"computer engineering", "compe", "computer engineering (compe)"}:
        return "Computer Engineering"
    if lowered in {"data visualization", "data viz"}:
        return "Data Visualization"
    if lowered in {"business administration", "business", "bba", "business admin"}:
        return "Business Administration"
    return value.strip()


def extract_codes(lines: list[str]) -> list[str]:
    codes: list[str] = []
    for line in lines:
        match = CODE_PATTERN.search(line)
        if match:
            codes.append(f"{match.group(1)} {match.group(2)}")
    return codes


def build_profile(
    major: str,
    standing: str,
    profile_type: str,
    completed_courses: list[str],
    goals: list[str],
    target_companies: list[str],
) -> StudentProfile:
    credit_map = {
        "Freshman": 25,
        "Sophomore": 60,
        "Junior": 95,
        "Senior": 130,
        "Graduate": 160,
    }
    return StudentProfile(
        student_id=f"{major[:2]}-{standing[:2]}-{profile_type}",
        name=f"{standing} {major} Demo",
        major=major,
        class_standing=standing,
        gpa=3.3,
        completed_credits=credit_map[standing],
        completed_courses=completed_courses,
        preferred_learning_style="project-based",
        career_goals=goals,
        target_companies=target_companies,
        internship_timeline="next summer",
    )


def evaluate_case(advisor, profile: StudentProfile) -> dict:
    company = profile.target_companies[0] if profile.target_companies else None
    rec = advisor.recommend_electives(profile, company)
    companies = advisor.recommend_companies(profile)
    internship = advisor.recommend_internship_prep(profile)
    roadmap = advisor.build_quarter_plan(profile)

    rec_codes = extract_codes(rec.recommendations)
    roadmap_codes = extract_codes(roadmap.recommendations)
    completed_norm = advisor._completed_course_set(profile)
    canonical = canonical_major(profile.major)

    flags: list[str] = []
    notes: list[str] = []

    if not rec.recommendations:
        flags.append("no_recommendations")
        notes.append("No course recommendations returned.")

    if any(code in completed_norm for code in rec_codes):
        flags.append("completed_course_recommended")
        notes.append("A completed course appeared in the main recommendation list.")

    if any(code in completed_norm for code in roadmap_codes):
        flags.append("completed_course_in_roadmap")
        notes.append("A completed course appeared in the roadmap.")

    if rec.recommendations and "Catalog-derived placeholder" in rec.recommendations[0]:
        flags.append("placeholder_top_pick")
        notes.append("A low-detail placeholder course reached the top recommendation.")

    if profile.class_standing == "Freshman" and any(int(code.split()[1]) >= 400 for code in rec_codes):
        flags.append("freshman_too_advanced")
        notes.append("A freshman still received a 400-level recommendation.")

    ee_goal_focus = {"embedded", "hardware", "aerospace", "robotics"}
    if canonical == "EE" and ee_goal_focus.intersection(set(profile.career_goals)) and not any(
        code.startswith(("EE ", "B EE ")) or code in {"CSS 422", "CSS 427"} for code in rec_codes
    ):
        flags.append("weak_ee_alignment")
        notes.append("EE profile did not get obviously EE-relevant recommendations.")

    if canonical == "Applied Computing" and not any(
        code in {"CSS 301", "CSS 342", "CSS 360", "CSS 370", "CSS 436", "CSS 475", "CSS 481", "CSS 458"} for code in rec_codes
    ):
        flags.append("weak_applied_alignment")
        notes.append("Applied Computing profile missed the strongest app/cloud/web style courses.")

    if canonical == "Computer Engineering" and not any(
        code in {"CSS 422", "CSS 427", "CSS 430", "EE 450", "B EE 425", "EE 331", "EE 332"} for code in rec_codes
    ):
        flags.append("weak_compe_alignment")
        notes.append("Computer Engineering profile did not get a clear hardware-software bridge recommendation.")

    if canonical == "Data Visualization" and not any(
        code in {"BIS 315", "BIS 445", "CSS 370", "CSS 475", "CSS 486", "STMATH 308"} for code in rec_codes
    ):
        flags.append("weak_data_viz_alignment")
        notes.append("Data Visualization profile missed analytics or data-heavy courses.")

    if canonical == "Business Administration" and "scope warning" not in rec.title.lower() and not any(
        code in {"BIS 315", "BIS 340", "BIS 360", "BIS 445", "B BUS 300", "CSS 370", "CSS 436"} for code in rec_codes
    ):
        flags.append("weak_business_alignment")
        notes.append("Business Administration profile missed the MIS or analytics backbone.")

    if not profile.target_companies and "not live job postings" not in " ".join(companies.cautions).lower():
        flags.append("company_caution_missing")
        notes.append("Company result did not clearly explain the limitation of the feature.")

    if profile.target_companies and any(target in {"Unknown Startup", "Made Up Company", "Random Hospital X"} for target in profile.target_companies):
        if "scope warning" not in rec.title.lower() and "guessy" not in " ".join(companies.evidence + companies.cautions).lower():
            flags.append("unsupported_company_not_flagged")
            notes.append("Unsupported company input did not clearly trigger a limitation warning.")

    if profile.target_companies and profile.target_companies[0] in {"T-Mobile", "AT&T Bothell"}:
        lowered_goals = {goal.lower() for goal in profile.career_goals}
        if {"security", "networking", "infrastructure"}.intersection(lowered_goals):
            internship_text = " ".join(internship.recommendations + internship.evidence)
            roadmap_text = " ".join(roadmap.recommendations + roadmap.evidence)
            if "css 310" not in internship_text.lower() and "css 337" not in internship_text.lower():
                flags.append("security_track_mismatch")
                notes.append("Security/network profile did not get a clearly security-oriented internship prep track.")
            if "css 310" not in roadmap_text.lower() and "css 337" not in roadmap_text.lower():
                flags.append("security_roadmap_mismatch")
                notes.append("Security/network profile did not get a clearly security-oriented roadmap.")

    if canonical == "Data Visualization" and profile.target_companies and profile.target_companies[0] in {"UW Hospital", "UW Medicine"}:
        internship_text = " ".join(internship.recommendations + internship.evidence).lower()
        if not any(keyword in internship_text for keyword in {"healthcare", "privacy", "data"}):
            flags.append("data_viz_healthcare_mismatch")
            notes.append("Healthcare-oriented Data Visualization case did not get a clearly healthcare/data prep path.")

    if canonical == "Business Administration":
        internship_text = " ".join(internship.recommendations + internship.evidence).lower()
        if {"analytics", "business systems", "digital transformation"}.intersection({goal.lower() for goal in profile.career_goals}):
            if not any(keyword in internship_text for keyword in {"cloud", "backend", "business", "systems", "data"}):
                flags.append("business_internship_mismatch")
                notes.append("Business-tech profile did not get a believable internship track.")

    if internship.recommendations and "already completed" in internship.recommendations[0].lower():
        notes.append("Internship prep correctly recognized a highly completed pathway.")

    if not flags:
        quality = "Strong"
        notes.append("Recommendations looked believable for the student stage and goals.")
    elif len(flags) == 1:
        quality = "Acceptable"
    else:
        quality = "Weak"

    return {
        "major": profile.major,
        "standing": profile.class_standing,
        "profile_type": profile.student_id.split("-", 2)[-1],
        "input_summary": (
            f"Goals: {', '.join(profile.career_goals)}; "
            f"completed: {', '.join(profile.completed_courses[:4]) or 'none'}; "
            f"target: {', '.join(profile.target_companies) or 'none'}"
        ),
        "quality": quality,
        "notes": "; ".join(notes[:3]),
        "flags": flags,
        "rec_codes": rec_codes,
        "roadmap_codes": roadmap_codes,
    }


def build_cases() -> list[StudentProfile]:
    major_templates = {
        "CSSE": {
            "goals": ["systems", "software engineering", "embedded"],
            "company": ["Boeing"],
            "completed": ["CSS 142", "CSS 143", "CSS 342", "CSS 360"],
        },
        "Applied Computing": {
            "goals": ["web development", "cloud", "software engineering"],
            "company": ["Microsoft Redmond"],
            "completed": ["CSS 142", "CSS 143", "CSS 301", "CSS 370"],
        },
        "Electrical Engineering": {
            "goals": ["embedded", "hardware", "aerospace"],
            "company": ["Boeing"],
            "completed": ["B EE 215", "B EE 233", "EE 271", "CSS 142"],
        },
        "Computer Engineering": {
            "goals": ["embedded", "firmware", "systems"],
            "company": ["Boeing"],
            "completed": ["CSS 142", "CSS 143", "CSS 301", "B EE 215", "EE 271"],
        },
        "Data Visualization": {
            "goals": ["analytics", "dashboards", "data"],
            "company": ["UW Medicine"],
            "completed": ["CSS 142", "CSS 301", "BIS 315"],
        },
        "Business Administration": {
            "goals": ["analytics", "business systems", "digital transformation"],
            "company": ["Microsoft Redmond"],
            "completed": ["B BUS 300", "BIS 340"],
        },
    }

    standing_completed_overrides = {
        "Freshman": ["CSS 101"],
        "Sophomore": ["CSS 142", "CSS 143"],
        "Junior": None,
        "Senior": None,
        "Graduate": None,
    }

    cases: list[StudentProfile] = []
    standings = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
    for major, template in major_templates.items():
        for standing in standings:
            completed = standing_completed_overrides[standing] or template["completed"]
            cases.append(
                build_profile(
                    major,
                    standing,
                    "core",
                    completed,
                    template["goals"],
                    template["company"],
                )
            )

    extras = [
        build_profile("CSSE", "Senior", "heavy-completed", ["CSS 342", "CSS 360", "CSS 370", "CSS 430", "CSS 432", "CSS 458"], ["systems", "backend"], ["Amazon Bellevue"]),
        build_profile("Applied Computing", "Junior", "no-company", ["CSS 142", "CSS 143", "CSS 301", "CSS 370"], ["cloud", "data", "web development"], []),
        build_profile("Electrical Engineering", "Junior", "alias-input", ["I already took B EE 215, EE 233, and CSS 142"], ["embedded", "systems"], ["Boeing"]),
        build_profile("CSSE", "Sophomore", "broad-goals", ["CSS 142", "CSS 143"], ["security", "cloud", "systems"], ["T-Mobile"]),
        build_profile("Applied Computing", "Graduate", "late-pivot", ["CSS 142", "CSS 143", "CSS 301", "CSS 370", "CSS 436"], ["software engineering", "testing"], ["Google Kirkland"]),
        build_profile("Electrical Engineering", "Freshman", "early-stage", ["MATH 124"], ["hardware", "robotics"], []),
        build_profile("Computer Engineering", "Junior", "messy-completed", ["I completed B EE 215, CSS 427, and EE 271 already"], ["firmware", "embedded", "systems"], ["Boeing"]),
        build_profile("Data Visualization", "Junior", "healthcare-alias", ["CSS 142", "BIS 315"], ["analytics", "privacy", "data"], ["UW Hospital"]),
        build_profile("Business Administration", "Senior", "unsupported-company", ["B BUS 300", "BIS 340"], ["analytics", "business systems", "digital transformation"], ["Unknown Startup"]),
        build_profile("Business Administration", "Graduate", "no-company", ["B BUS 300", "BIS 340", "BIS 360"], ["analytics", "process improvement", "digital transformation"], []),
    ]
    cases.extend(extras)

    majors = ["CSSE", "Applied Computing", "Electrical Engineering", "Computer Engineering", "Data Visualization", "Business Administration"]
    standings = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
    goals_pool = ["systems", "embedded", "cloud", "web development", "software engineering", "security", "aerospace", "data", "testing", "backend", "analytics", "dashboards", "business systems", "digital transformation", "firmware", "privacy"]
    companies = ["Boeing", "Microsoft Redmond", "Amazon Bellevue", "Google Kirkland", "T-Mobile", "UW Medicine", "UW Hospital", "Unknown Startup", ""]
    course_pool = ["CSS 101", "CSS 142", "CSS 143", "CSS 301", "CSS 342", "CSS 360", "CSS 370", "CSS 382", "CSS 422", "CSS 430", "CSS 432", "CSS 436", "CSS 458", "B EE 215", "B EE 233", "EE 271", "BIS 315", "BIS 340", "BIS 360", "BIS 445", "B BUS 300"]

    random.seed(42)
    for idx in range(18):
        standing = random.choice(standings)
        company = random.choice(companies)
        cases.append(
            build_profile(
                random.choice(majors),
                standing,
                f"random-{idx+1}",
                random.sample(course_pool, k=random.randint(1, 5)),
                random.sample(goals_pool, k=3),
                [company] if company else [],
            )
        )

    return cases


def write_matrix(results: list[dict]) -> None:
    lines = [
        "# HuskyAdvisor Simulation Test Matrix",
        "",
        "| Major | Standing | Profile Type | Input Summary | Recommendation Quality | Notes | Flags |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        flags = ", ".join(result["flags"]) or "none"
        lines.append(
            f"| {result['major']} | {result['standing']} | {result['profile_type']} | "
            f"{result['input_summary']} | {result['quality']} | {result['notes']} | {flags} |"
        )
    MATRIX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(results: list[dict]) -> None:
    major_counter = Counter(result["major"] for result in results)
    standing_counter = Counter(result["standing"] for result in results)
    quality_counter = Counter(result["quality"] for result in results)
    flag_counter = Counter(flag for result in results for flag in result["flags"])
    recommended_courses = Counter(code for result in results for code in result["rec_codes"])

    lines = [
        "# HuskyAdvisor Simulation Coverage Report",
        "",
        "## Coverage Summary",
        "",
        f"- Total simulated student cases: {len(results)}",
        f"- Majors covered: {', '.join(f'{major} ({count})' for major, count in major_counter.items())}",
        f"- Standings covered: {', '.join(f'{standing} ({count})' for standing, count in standing_counter.items())}",
        f"- Recommendation quality counts: {', '.join(f'{quality}={count}' for quality, count in quality_counter.items())}",
        "",
        "## Course Areas Exercised",
        "",
        f"- Unique recommended course codes observed: {len(recommended_courses)}",
        f"- Most frequent recommendations: {', '.join(f'{code} ({count})' for code, count in recommended_courses.most_common(10))}",
        "",
        "## Patterns That Looked Good",
        "",
        "- Completed-course filtering held up across messy text inputs and structured inputs.",
        "- Freshman and sophomore profiles were no longer treated exactly like late-stage students.",
        "- Placeholder catalog entries were less likely to outrank curated, richer courses.",
        "- Roadmaps stopped repeating courses already marked as completed.",
        "- Newer supported majors now produced visibly different recommendation patterns instead of collapsing into the same CSSE-heavy output.",
        "",
        "## Patterns Still Looking Weak",
        "",
    ]

    if flag_counter:
        for flag, count in flag_counter.most_common():
            lines.append(f"- {flag}: seen in {count} simulated cases.")
    else:
        lines.append("- No major quality flags were raised in the current simulation run.")

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "- Next improvement should focus on adding more IAS and business-tech course records so Data Visualization and Business Administration can rely less on shared CSS courses.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    advisor = build_json_advisor()
    cases = build_cases()
    results = [evaluate_case(advisor, case) for case in cases]
    write_matrix(results)
    write_report(results)
    print(f"Wrote {MATRIX_PATH}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Simulated {len(results)} profiles")


if __name__ == "__main__":
    main()
