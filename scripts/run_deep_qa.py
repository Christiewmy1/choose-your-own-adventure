from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from fastapi.testclient import TestClient

from api.main import app
from huskyadvisor.models import StudentProfile
from huskyadvisor.service import build_json_advisor


REPORT_PATH = ROOT / "docs" / "deep_qa_500_scenario_report.md"
CODE_PATTERN = re.compile(r"\b([A-Z]{2,6}|[A-Z]\s+[A-Z]{2,6})\s*-?\s*(\d{3})\b")

SUPPORTED_MAJORS = [
    "CSSE",
    "Computer Science and Software Engineering",
    "Applied Computing",
    "Electrical Engineering",
    "Computer Engineering",
    "Data Visualization",
    "Business Administration",
]
UNSUPPORTED_MAJORS = ["Informatics", "Biology", "Psychology", "Mechanical Engineering"]
STANDINGS = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
GOAL_SETS = [
    ["cloud", "software engineering", "backend"],
    ["security", "networking", "infrastructure"],
    ["embedded", "aerospace", "systems"],
    ["analytics", "dashboards", "data"],
    ["business systems", "digital transformation", "product"],
    ["healthcare", "privacy", "data"],
    ["gaming", "graphics", "interactive software"],
    ["ai", "machine learning", "data"],
    ["financial technology", "security", "cloud"],
    ["retail tech", "e-commerce", "analytics"],
    ["streaming media", "distributed systems", "data"],
    ["automotive software", "embedded", "cloud"],
    ["consumer platforms", "mobile", "backend"],
]
COMPLETED_SETS = [
    [],
    ["CSS 142"],
    ["CSS 142", "CSS 143"],
    ["CSS 142", "CSS 143", "CSS 301", "CSS 370"],
    ["I already took CSS430 and css458", "CSS-481", "B EE 215"],
    ["CSS 342", "CSS 360", "CSS 370", "CSS 430", "CSS 436", "CSS 458", "CSS 481"],
    ["B BUS 300", "BIS 315", "BIS 340", "BIS 360"],
    ["B EE 215", "B EE 233", "EE 271", "CSS 142"],
]
NEW_SOFTWARE_EMPLOYERS = [
    "IBM",
    "Netflix",
    "Uber",
    "Airbnb",
    "Walmart Global Tech",
    "JPMorgan Chase Technology",
    "Capital One Technology",
    "Visa Technology",
    "Mastercard Technology",
    "Target Tech",
    "Home Depot Technology",
    "Disney Streaming",
    "Intuit",
    "Tesla Software",
    "Ford Pro Software",
    "General Motors Software",
    "Nike Technology",
    "The Trade Desk",
    "DoorDash",
    "Pinterest",
]
CORE_EMPLOYERS = [
    "Boeing",
    "Microsoft Redmond",
    "Amazon Bellevue",
    "Google Kirkland",
    "T-Mobile",
    "UW Medicine",
    "UW Hospital",
    "Nintendo of America",
    "",
]
UNSUPPORTED_COMPANIES = ["Unknown Startup", "Random Hospital X", "Imaginary AI Lab"]
INTENT_ALIASES = ["fintech", "retail tech", "consumer software", "connected vehicles", "payments"]


@dataclass
class ScenarioResult:
    scenario_id: str
    major: str
    standing: str
    company: str
    goals: list[str]
    quality: str = "pass"
    failures: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    recommendation_codes: list[str] = field(default_factory=list)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def extract_codes(items: Iterable[str]) -> list[str]:
    codes: list[str] = []
    for item in items:
        for department, number in CODE_PATTERN.findall(item.upper()):
            normalized = " ".join(f"{department} {number}".split())
            if normalized not in codes:
                codes.append(normalized)
    return codes


def normalized_completed(advisor, profile: StudentProfile) -> set[str]:
    return advisor._completed_course_set(profile)


def build_profile(index: int, major: str, standing: str, goals: list[str], company: str, completed: list[str]) -> StudentProfile:
    credits = {
        "Freshman": 25,
        "Sophomore": 65,
        "Junior": 95,
        "Senior": 130,
        "Graduate": 160,
    }[standing]
    return StudentProfile(
        student_id=f"deep-qa-{index:04d}",
        name=f"Deep QA Student {index}",
        major=major,
        class_standing=standing,
        gpa=3.3,
        completed_credits=credits,
        completed_courses=completed,
        preferred_learning_style="project-based",
        career_goals=goals,
        target_companies=[company] if company else [],
        internship_timeline="next summer",
    )


def build_scenarios(limit: int) -> list[StudentProfile]:
    companies = CORE_EMPLOYERS + NEW_SOFTWARE_EMPLOYERS + INTENT_ALIASES + UNSUPPORTED_COMPANIES
    majors = SUPPORTED_MAJORS + UNSUPPORTED_MAJORS
    scenarios: list[StudentProfile] = []
    index = 1

    for major in majors:
        for standing in STANDINGS:
            for goals in GOAL_SETS:
                company = companies[(index - 1) % len(companies)]
                completed = COMPLETED_SETS[(index - 1) % len(COMPLETED_SETS)]
                scenarios.append(build_profile(index, major, standing, goals, company, completed))
                index += 1
                if len(scenarios) >= limit:
                    return scenarios

    return scenarios


def evaluate_profile(advisor, profile: StudentProfile) -> ScenarioResult:
    target = profile.target_companies[0] if profile.target_companies else None
    result = ScenarioResult(
        scenario_id=profile.student_id,
        major=profile.major,
        standing=profile.class_standing,
        company=target or "none",
        goals=profile.career_goals,
    )

    course_result = advisor.recommend_electives(profile, target)
    company_result = advisor.recommend_companies(profile)
    internship_result = advisor.recommend_internship_prep(profile)
    roadmap_result = advisor.build_quarter_plan(profile)
    major_result = advisor.suggest_major(profile.career_goals)

    all_results = [course_result, company_result, internship_result, roadmap_result, major_result]
    for section in all_results:
        if not section.title or not section.summary:
            result.failures.append("missing_title_or_summary")
        if section.title.lower().endswith("scope warning"):
            result.observations.append("scope_warning_seen")

    scope_expected = profile.major in UNSUPPORTED_MAJORS or target in UNSUPPORTED_COMPANIES
    if scope_expected:
        scope_text = " ".join(course_result.evidence + course_result.cautions + course_result.recommendations).lower()
        if "misleading" not in scope_text and "outside the current supported" not in scope_text and "guessy" not in scope_text:
            result.failures.append("unsupported_scope_not_honest")
    else:
        if not course_result.recommendations:
            result.failures.append("empty_course_recommendations")
        if not company_result.recommendations:
            result.failures.append("empty_company_recommendations")

    completed = normalized_completed(advisor, profile)
    rec_codes = extract_codes(course_result.recommendations)
    roadmap_codes = extract_codes(roadmap_result.recommendations)
    result.recommendation_codes = rec_codes
    repeated = sorted((set(rec_codes) | set(roadmap_codes)).intersection(completed))
    if repeated:
        result.failures.append(f"completed_courses_repeated:{','.join(repeated)}")

    if target in NEW_SOFTWARE_EMPLOYERS and not scope_expected:
        course_text = " ".join(course_result.recommendations + course_result.evidence).lower()
        company_text = " ".join(company_result.recommendations + company_result.evidence).lower()
        if target.lower() not in course_text and target.lower() not in company_text:
            result.failures.append("new_company_target_not_reflected")

    if target in INTENT_ALIASES and not scope_expected:
        joined = " ".join(course_result.recommendations + course_result.evidence).lower()
        if not any(token in joined for token in ["target company/field resolved", "explicitly mapped", "overlaps", "relevant"]):
            result.failures.append("intent_alias_not_influencing_courses")

    if not any("not live" in caution.lower() or "live job" in caution.lower() for caution in company_result.cautions):
        result.failures.append("company_live_job_caution_missing")

    if "security" in {goal.lower() for goal in profile.career_goals} and target in {"T-Mobile", "AT&T Bothell"}:
        security_text = " ".join(internship_result.recommendations + roadmap_result.recommendations).lower()
        if "css 310" not in security_text and "css 337" not in security_text and "security" not in security_text:
            result.failures.append("security_goal_not_reflected")

    if result.failures:
        result.quality = "fail"
    return result


def evaluate_api_contract() -> list[str]:
    failures: list[str] = []
    client = TestClient(app)
    payload = {
        "major": "Computer Science and Software Engineering",
        "class_standing": "Junior",
        "completed_courses": ["CSS 142", "CSS 143", "CSS 301"],
        "career_goals": ["cloud", "software engineering"],
        "target_companies": ["JPMorgan Chase Technology"],
    }
    for path in [
        "/api/profile/recommendations",
        "/api/profile/companies",
        "/api/profile/internship-prep",
        "/api/profile/roadmap",
        "/api/profile/major",
    ]:
        response = client.post(path, json=payload)
        if response.status_code != 200:
            failures.append(f"{path}:status_{response.status_code}")
            continue
        data = response.json()
        trace = data.get("ai_trace", {})
        if not trace:
            failures.append(f"{path}:missing_ai_trace")
        if "Crawl4AI" not in trace.get("data_ingestion", ""):
            failures.append(f"{path}:missing_crawl4ai_trace")
        if trace.get("fallback_mode") is not False:
            failures.append(f"{path}:unexpected_fallback_trace")
    if client.get("/api/profile/recommendations").status_code != 405:
        failures.append("post_only_route_not_405")
    return failures


def evaluate_data_integrity() -> list[str]:
    failures: list[str] = []
    companies = load_json("data/local_tech_companies.json").get("companies", [])
    mappings = load_json("data/company_course_mapping.json").get("mappings", [])
    intent_profiles = load_json("data/company_intent_profiles.json").get("profiles", [])
    targets = load_json("data/crawl4ai/targets/seed_targets.json").get("targets", [])
    company_names = {company["name"] for company in companies}
    mapped_names = {mapping["company"] for mapping in mappings}

    if len(companies) < 140:
        failures.append(f"company_count_too_low:{len(companies)}")
    if len(mappings) < len(companies):
        failures.append(f"mapping_count_less_than_company_count:{len(mappings)}<{len(companies)}")
    missing_mapping = sorted(company_names - mapped_names)
    if missing_mapping:
        failures.append(f"companies_missing_course_mapping:{missing_mapping[:5]}")
    for expected in NEW_SOFTWARE_EMPLOYERS:
        if expected not in company_names:
            failures.append(f"missing_new_company:{expected}")
        if expected not in mapped_names:
            failures.append(f"missing_new_company_mapping:{expected}")
    if len(intent_profiles) < 7:
        failures.append("intent_profile_count_too_low")
    if not targets:
        failures.append("crawl4ai_targets_empty")
    if not (ROOT / "data" / "crawl4ai" / "raw").exists() or not (ROOT / "data" / "crawl4ai" / "normalized").exists():
        failures.append("crawl4ai_raw_normalized_dirs_missing")
    return failures


def evaluate_public_backend() -> list[str]:
    failures: list[str] = []

    def curl_json(url: str, payload: dict | None = None) -> tuple[int, dict | None, str]:
        command = ["curl", "-s", "-i"]
        if payload is not None:
            command.extend(
                [
                    "-X",
                    "POST",
                    url,
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    json.dumps(payload),
                ]
            )
        else:
            command.append(url)
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)
        if completed.returncode != 0:
            return completed.returncode, None, completed.stderr.strip() or completed.stdout.strip()
        headers, _, body = completed.stdout.partition("\r\n\r\n")
        status_match = re.search(r"HTTP/\S+\s+(\d+)", headers)
        status = int(status_match.group(1)) if status_match else 0
        try:
            return status, json.loads(body), ""
        except json.JSONDecodeError:
            return status, None, body[:200]

    health_status, health_body, health_error = curl_json("https://choose-your-own-adventure-bay.vercel.app/health")
    if health_status != 200 or health_body != {"status": "ok"}:
        failures.append(f"public_health_failed:status={health_status}:error={health_error}")

    payload = {
        "major": "Computer Science and Software Engineering",
        "class_standing": "Junior",
        "completed_courses": ["CSS 142", "CSS 143"],
        "career_goals": ["cloud", "software engineering"],
        "target_companies": ["JPMorgan Chase Technology"],
    }
    post_status, data, post_error = curl_json(
        "https://choose-your-own-adventure-bay.vercel.app/api/profile/recommendations",
        payload,
    )
    if post_status != 200 or not data:
        failures.append(f"public_post_failed:status={post_status}:error={post_error}")
        return failures
    if "recommendations" not in data:
        failures.append("public_post_missing_recommendations")
    if "ai_trace" not in data:
        failures.append("public_post_missing_ai_trace")
    public_text = json.dumps(data)
    if "JPMorgan Chase Technology" not in public_text or "Scope Warning" in data.get("title", ""):
        failures.append("public_backend_stale_missing_expanded_company_dataset")
    return failures


def write_report(
    scenario_results: list[ScenarioResult],
    api_failures: list[str],
    data_failures: list[str],
    public_failures: list[str],
    public_checked: bool,
) -> None:
    failure_counter = Counter(failure.split(":", 1)[0] for result in scenario_results for failure in result.failures)
    major_counter = Counter(result.major for result in scenario_results)
    standing_counter = Counter(result.standing for result in scenario_results)
    company_counter = Counter(result.company for result in scenario_results)
    goal_counter = Counter(goal for result in scenario_results for goal in result.goals)
    course_counter = Counter(code for result in scenario_results for code in result.recommendation_codes)
    failed_scenarios = [result for result in scenario_results if result.failures]

    lines = [
        "# Deep QA 500+ Scenario Report",
        "",
        "## Summary",
        "",
        f"- Scenario profiles tested: {len(scenario_results)}",
        f"- Passed scenarios: {len(scenario_results) - len(failed_scenarios)}",
        f"- Failed scenarios: {len(failed_scenarios)}",
        f"- API contract failures: {len(api_failures)}",
        f"- Data integrity failures: {len(data_failures)}",
        f"- Public backend check failures: {len(public_failures) if public_checked else 'not run in this local-only report'}",
        "",
        "## Coverage",
        "",
        f"- Majors covered: {', '.join(f'{major} ({count})' for major, count in major_counter.items())}",
        f"- Standings covered: {', '.join(f'{standing} ({count})' for standing, count in standing_counter.items())}",
        f"- Unique target company/field inputs: {len(company_counter)}",
        f"- Goal tags covered: {', '.join(f'{goal} ({count})' for goal, count in goal_counter.most_common())}",
        f"- Unique recommended course codes observed: {len(course_counter)}",
        f"- Most common course recommendations: {', '.join(f'{code} ({count})' for code, count in course_counter.most_common(12))}",
        "",
        "## Failure Types",
        "",
    ]
    if failure_counter:
        lines.extend(f"- {failure}: {count}" for failure, count in failure_counter.most_common())
    else:
        lines.append("- No scenario-level invariant failures.")

    lines.extend(["", "## API Contract Check", ""])
    lines.extend([f"- {failure}" for failure in api_failures] or ["- Passed."])
    lines.extend(["", "## Data Integrity Check", ""])
    lines.extend([f"- {failure}" for failure in data_failures] or ["- Passed."])
    lines.extend(["", "## Public Backend Check", ""])
    if public_checked:
        lines.extend([f"- {failure}" for failure in public_failures] or ["- Passed."])
    else:
        lines.append("- Skipped in this deterministic local run. Use `python3 scripts/run_deep_qa.py --scenarios 560 --public` after redeploying the backend.")

    lines.extend(["", "## First 25 Failed Scenarios", ""])
    if failed_scenarios:
        lines.append("| Scenario | Major | Standing | Company | Goals | Failures |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for result in failed_scenarios[:25]:
            lines.append(
                f"| {result.scenario_id} | {result.major} | {result.standing} | {result.company} | "
                f"{', '.join(result.goals)} | {', '.join(result.failures)} |"
            )
    else:
        lines.append("- No failed scenarios.")

    lines.extend(
        [
            "",
            "## Honest Weak Spots",
            "",
            "- This stress test validates deterministic engine behavior and API shape; it does not prove official degree accuracy.",
            "- Public endpoint checks depend on current network availability and deployment state.",
            "- Crawl4AI is validated as a data-ingestion/normalization pipeline; crawled facts still require human review before becoming trusted advising data.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run HuskyAdvisor deep QA simulation.")
    parser.add_argument("--scenarios", type=int, default=560, help="Number of simulated profiles to evaluate.")
    parser.add_argument("--public", action="store_true", help="Also test deployed public backend endpoints.")
    args = parser.parse_args()

    advisor = build_json_advisor()
    profiles = build_scenarios(args.scenarios)
    scenario_results = [evaluate_profile(advisor, profile) for profile in profiles]
    api_failures = evaluate_api_contract()
    data_failures = evaluate_data_integrity()
    public_failures = evaluate_public_backend() if args.public else []
    write_report(scenario_results, api_failures, data_failures, public_failures, args.public)

    total_failures = (
        sum(len(result.failures) for result in scenario_results)
        + len(api_failures)
        + len(data_failures)
        + len(public_failures)
    )
    print(f"Scenario profiles tested: {len(scenario_results)}")
    print(f"Scenario failures: {sum(1 for result in scenario_results if result.failures)}")
    print(f"API contract failures: {len(api_failures)}")
    print(f"Data integrity failures: {len(data_failures)}")
    print(f"Public backend failures: {len(public_failures)}")
    print(f"Wrote {REPORT_PATH}")
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
