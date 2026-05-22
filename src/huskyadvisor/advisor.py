from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, List

from huskyadvisor.models import AdvisingResult, CompanyRecord, CourseRecord, MajorRecord, StudentProfile


@dataclass
class ScoredCourse:
    course: CourseRecord
    score: int
    evidence: List[str]


class HuskyAdvisorEngine:
    def __init__(
        self,
        majors: Iterable[MajorRecord],
        courses: Iterable[CourseRecord],
        companies: Iterable[CompanyRecord],
        recent_offerings: dict[str, list[str]] | None = None,
        company_course_mapping: dict[str, list[str]] | None = None,
        internship_playbooks: list[dict] | None = None,
        quarter_plan_templates: list[dict] | None = None,
    ) -> None:
        self.majors = list(majors)
        self.courses = list(courses)
        self.companies = list(companies)
        self.recent_offerings = recent_offerings or {}
        self.company_course_mapping = company_course_mapping or {}
        self.internship_playbooks = internship_playbooks or []
        self.quarter_plan_templates = quarter_plan_templates or []

    def recommend_electives(self, profile: StudentProfile, target_company: str | None = None) -> AdvisingResult:
        company = self._find_company(target_company or self._first_or_none(profile.target_companies))
        scored = self._score_elective_courses(profile, company)
        top_courses = scored[:3]

        recommendations = [
            f"{item.course.course_code} {item.course.title}: {item.course.description}" for item in top_courses
        ]
        evidence = [reason for item in top_courses for reason in item.evidence[:2]]
        cautions = [
            f"Check prerequisites for {item.course.course_code}: {item.course.prerequisite_text}."
            for item in top_courses
        ]

        summary = (
            f"For a {profile.class_standing} {profile.major} student targeting "
            f"{company.name if company else 'local technical roles'}, these next-step electives best balance fit,"
            " realism, and preparation value."
        )

        return AdvisingResult(
            title="Recommended 400-Level Electives",
            summary=summary,
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def recommend_companies(self, profile: StudentProfile) -> AdvisingResult:
        ranked: list[tuple[int, CompanyRecord, list[str]]] = []
        for company in self.companies:
            score = 0
            evidence: list[str] = []

            goal_overlap = self._overlap(company.target_skills, profile.career_goals)
            if goal_overlap:
                score += 2 * len(goal_overlap)
                evidence.append(
                    f"{company.name} matches your goals through skills like {', '.join(goal_overlap)}."
                )

            relevant_courses = [
                course.course_code
                for course in self.courses
                if profile.major in course.major_tags
                and self._overlap(course.career_tags, company.target_skills)
            ]
            if relevant_courses:
                score += min(3, len(relevant_courses))
                evidence.append(
                    f"Your program already connects to {company.name} through courses like {', '.join(relevant_courses[:3])}."
                )

            if company.name in profile.target_companies:
                score += 2
                evidence.append(f"{company.name} is already one of your stated target companies.")

            ranked.append((score, company, evidence))

        ranked.sort(key=lambda item: item[0], reverse=True)
        top = ranked[:3]

        recommendations = [
            f"{company.name} ({company.city}): focus on {company.domain_focus}. Hiring often appears around {', '.join(company.hiring_seasons)}."
            for _, company, _ in top
        ]
        evidence = [reason for _, _, reasons in top for reason in reasons[:2]]
        cautions = [
            "These are company-alignment suggestions, not live job postings.",
            "Internship timing and openings can change each term, so live postings should still be checked separately.",
        ]

        return AdvisingResult(
            title="Local Company Alignment",
            summary="These companies best match your current academic path and stated goals.",
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def recommend_internship_prep(self, profile: StudentProfile) -> AdvisingResult:
        lowered_goals = [goal.lower() for goal in profile.career_goals]
        selected = None
        for playbook in self.internship_playbooks:
            track = playbook.get("track", "").lower()
            if any(token in " ".join(lowered_goals) for token in track.split("_")):
                selected = playbook
                break

        if selected is None and self.internship_playbooks:
            selected = self.internship_playbooks[0]

        if selected is None:
            return AdvisingResult(
                title="Internship Prep Plan",
                summary="No internship prep playbooks are currently loaded.",
            )

        completed = self._completed_course_set(profile)
        remaining_courses = [
            code
            for code in selected.get("recommended_courses", [])
            if self._normalize_code(code) not in completed
        ]
        if not remaining_courses:
            remaining_courses = ["You have already completed the main recommended courses for this track."]

        next_project = selected.get("recommended_projects", [])
        next_skills = selected.get("recommended_skills", [])
        target_companies = selected.get("target_companies", [])
        target_hint = (
            f" aligned with {profile.target_companies[0]}"
            if profile.target_companies
            else ""
        )

        recommendations = [
            f"Recommended next courses{target_hint}: {', '.join(remaining_courses)}",
            *next_project,
        ]
        evidence = [
            f"Target companies in this playbook: {', '.join(target_companies)}.",
            f"Suggested skills to strengthen: {', '.join(next_skills)}.",
            f"Completed courses already considered: {', '.join(profile.completed_courses) or 'none listed'}.",
        ]
        cautions = [
            "This is a preparation guide, not a live internship feed.",
            "Use this together with current job boards and official internship postings.",
        ]
        return AdvisingResult(
            title="Internship Prep Plan",
            summary="This plan highlights the remaining courses, projects, and skills that best fit one likely internship pathway for your profile.",
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def suggest_major(self, interests: List[str]) -> AdvisingResult:
        ranked: list[tuple[int, MajorRecord]] = []
        for major in self.majors:
            overlap = self._overlap([item.lower() for item in major.best_for], [item.lower() for item in interests])
            ranked.append((len(overlap), major))

        ranked.sort(key=lambda item: item[0], reverse=True)
        best_score, best_major = ranked[0]
        recommendations = [
            f"{best_major.major_name} ({best_major.degree_type}): {best_major.summary}",
            f"Typical courses: {', '.join(best_major.typical_courses)}",
            f"Common career paths: {', '.join(best_major.career_paths)}",
        ]
        evidence = [
            f"Matched interests: {', '.join(self._overlap(best_major.best_for, interests)) or 'broad software alignment'}."
        ]
        cautions = []
        if best_score == 0:
            cautions.append("Your interests are broad, so this recommendation should be treated as exploratory.")

        return AdvisingResult(
            title="Suggested Major Path",
            summary=f"{best_major.major_name} looks like the strongest current fit based on your stated interests.",
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def build_quarter_plan(self, profile: StudentProfile) -> AdvisingResult:
        selected_template = self._select_quarter_template(profile)
        completed = self._completed_course_set(profile)
        used_codes: set[str] = set()
        if selected_template:
            replacement_pool = [
                item.course.course_code
                for item in self._score_elective_courses(
                    profile,
                    self._find_company(self._first_or_none(profile.target_companies)),
                )
            ]
            next_steps: list[str] = []
            filtered_any_completed = False

            for quarter in selected_template.get("quarters", []):
                kept_codes: list[str] = []
                for code in quarter.get("course_suggestions", []):
                    normalized = self._normalize_code(code)
                    if normalized in completed:
                        filtered_any_completed = True
                        continue
                    if normalized not in used_codes:
                        kept_codes.append(code)
                        used_codes.add(normalized)

                for code in replacement_pool:
                    normalized = self._normalize_code(code)
                    if normalized in completed or normalized in used_codes:
                        continue
                    if len(kept_codes) >= len(quarter.get("course_suggestions", [])):
                        break
                    kept_codes.append(code)
                    used_codes.add(normalized)

                if not kept_codes:
                    kept_codes = ["Use this quarter for project depth, interview prep, and an approved advisor-reviewed elective."]

                next_steps.append(
                    (
                        f"{quarter['label']}: {quarter['focus']}. "
                        f"Suggested courses: {', '.join(kept_codes)}. "
                        f"Project goal: {quarter['project_goal']}"
                    )
                )

            next_steps = [
                step
                for step in next_steps
            ]
            evidence = [
                f"This roadmap was selected because your goals overlap with the {selected_template.get('track', 'general')} track.",
                f"Target companies in this track: {', '.join(selected_template.get('recommended_companies', []))}.",
            ]
            if filtered_any_completed:
                evidence.append("Completed courses were removed from the roadmap and replaced with remaining options when possible.")
            summary = "This roadmap matches one of HuskyAdvisor's structured preparation tracks."
        else:
            next_steps = [
                "Quarter 1: Take one systems-oriented elective and build a small class-aligned project with tests.",
                "Quarter 2: Strengthen teamwork experience through a larger software project and resume-ready documentation.",
                "Quarter 3: Tailor a project toward your target industry, such as aerospace reliability or embedded software.",
            ]
            evidence = [
                f"You already completed: {', '.join(profile.completed_courses)}.",
                f"Your target companies include: {', '.join(profile.target_companies) or 'regional employers'}.",
            ]
            summary = "This roadmap focuses on building internship-ready systems experience without overloading the MVP."

        cautions = [
            "Confirm prerequisite sequencing with an advisor before treating this as an official degree plan.",
        ]
        return AdvisingResult(
            title="Quarter-by-Quarter Success Roadmap",
            summary=summary,
            recommendations=next_steps,
            evidence=evidence,
            cautions=cautions,
        )

    def _score_elective_courses(
        self,
        profile: StudentProfile,
        company: CompanyRecord | None = None,
    ) -> List[ScoredCourse]:
        scored: List[ScoredCourse] = []
        completed = self._completed_course_set(profile)

        for course in self.courses:
            if course.level < 400 or course.level >= 500:
                continue
            if self._normalize_code(course.course_code) in completed:
                continue

            score = 0
            evidence: List[str] = []

            if profile.major in course.major_tags:
                score += 3
                evidence.append(f"{course.course_code} is tagged for {profile.major}.")

            score += self._quality_score_adjustment(course, evidence)

            recent_terms = self.recent_offerings.get(course.course_code, [])
            if recent_terms:
                score += 1
                evidence.append(
                    f"{course.course_code} appeared in recent terms: {', '.join(recent_terms)}."
                )

            if company:
                mapped_courses = self.company_course_mapping.get(company.name, [])
                if course.course_code in mapped_courses:
                    score += 2
                    evidence.append(f"{course.course_code} is explicitly mapped to {company.name} in the career dataset.")

                shared_skills = self._overlap(course.career_tags, company.target_skills)
                if shared_skills:
                    score += 2 * len(shared_skills)
                    evidence.append(
                        f"{course.course_code} overlaps with {company.name} skills: {', '.join(shared_skills)}."
                    )

                if "aerospace" in course.career_tags and "aerospace" in company.domain_focus.lower():
                    score += 2
                    evidence.append(f"{course.course_code} directly aligns with aerospace-oriented work.")

            goal_overlap = self._overlap(course.career_tags, profile.career_goals)
            if goal_overlap:
                score += len(goal_overlap)
                evidence.append(f"It supports your stated goals: {', '.join(goal_overlap)}.")

            if profile.preferred_learning_style.lower().startswith("project") and course.project_emphasis == "high":
                score += 1
                evidence.append("This course has strong project emphasis, which matches your learning style.")

            score += self._readiness_adjustment(profile, course, completed, evidence)

            scored.append(ScoredCourse(course=course, score=score, evidence=evidence))

        scored.sort(
            key=lambda item: (
                item.score,
                self._quality_rank(item.course),
                len(self.recent_offerings.get(item.course.course_code, [])),
                item.course.course_code,
            ),
            reverse=True,
        )
        return scored

    def _quality_score_adjustment(self, course: CourseRecord, evidence: List[str]) -> int:
        bonus = 0
        source_type = course.source_type.lower()
        confidence = course.source_confidence.lower()
        description = course.description.lower()

        if source_type == "curated_uwb_snapshot":
            bonus += 3
            evidence.append("This course comes from a richer curated HuskyAdvisor dataset entry.")
        elif source_type == "catalog_derived_plus_curated":
            bonus += 2
        elif source_type == "catalog_schedule_derived":
            bonus -= 1

        if confidence == "high":
            bonus += 2
        elif confidence == "medium-high":
            bonus += 1

        if "catalog-derived placeholder" in description:
            bonus -= 3
            evidence.append("This course is still using placeholder catalog metadata, so it is ranked more cautiously.")

        return bonus

    def _quality_rank(self, course: CourseRecord) -> int:
        rank = 0
        if course.source_type == "curated_uwb_snapshot":
            rank += 3
        elif course.source_type == "catalog_derived_plus_curated":
            rank += 2
        elif course.source_type == "catalog_schedule_derived":
            rank += 1

        if course.source_confidence == "high":
            rank += 2
        elif course.source_confidence == "medium-high":
            rank += 1

        if "catalog-derived placeholder" in course.description.lower():
            rank -= 2

        return rank

    def _readiness_adjustment(
        self,
        profile: StudentProfile,
        course: CourseRecord,
        completed: set[str],
        evidence: List[str],
    ) -> int:
        adjustment = 0
        prereqs = self._extract_prereq_courses(course.prerequisite_text)
        prereq_ready = all(token in completed for token in prereqs)
        if prereq_ready:
            adjustment += 1
            evidence.append("Your completed courses suggest you are reasonably prepared.")
        else:
            adjustment -= 2
            evidence.append("You may need to verify prerequisites before enrolling.")

        if profile.completed_credits < 75:
            adjustment -= 2
            evidence.append("This looks more like a future-planning elective than an immediate next-quarter course at your current credit level.")
        elif profile.completed_credits < 90 and course.level >= 480:
            adjustment -= 1
            evidence.append("This course may fit better after a bit more upper-division progress.")

        return adjustment

    def _find_company(self, name: str | None) -> CompanyRecord | None:
        if not name:
            return None
        lowered = name.lower()
        for company in self.companies:
            if company.name.lower() == lowered:
                return company
        return None

    def _select_quarter_template(self, profile: StudentProfile) -> dict | None:
        if not self.quarter_plan_templates:
            return None

        lowered_goals = [goal.lower() for goal in profile.career_goals]
        best_template: dict | None = None
        best_score = -1
        for template in self.quarter_plan_templates:
            keywords = [keyword.lower() for keyword in template.get("goal_keywords", [])]
            score = len(self._overlap(keywords, lowered_goals))
            if score > best_score:
                best_score = score
                best_template = template

        return best_template if best_score > 0 else self.quarter_plan_templates[0]

    def _normalize_code(self, value: str) -> str:
        return " ".join(value.strip().upper().split())

    def _completed_course_set(self, profile: StudentProfile) -> set[str]:
        completed: set[str] = set()
        for value in profile.completed_courses:
            normalized = self._normalize_code(value)
            if normalized:
                completed.add(normalized)
            completed.update(self._extract_course_codes_from_text(value))
        return completed

    def _extract_course_codes_from_text(self, value: str) -> set[str]:
        pattern = re.compile(r"\b([A-Z]{2,6}|[A-Z]\s+[A-Z]{2,6})\s*-?\s*(\d{3})\b")
        matches = pattern.findall(value.upper())
        return {
            self._normalize_code(f"{department} {number}")
            for department, number in matches
        }

    @staticmethod
    def _overlap(left: Iterable[str], right: Iterable[str]) -> List[str]:
        left_map = {item.lower(): item for item in left}
        right_set = {item.lower() for item in right}
        return [original for key, original in left_map.items() if key in right_set]

    @staticmethod
    def _extract_prereq_courses(prerequisite_text: str) -> List[str]:
        known_prefixes = ("CSS ", "EE ", "BIS ")
        tokens = prerequisite_text.replace(",", " ").split()
        results: List[str] = []
        for index, token in enumerate(tokens[:-1]):
            spaced = f"{token} {tokens[index + 1]}"
            if token in {"CSS", "EE", "BIS"} and tokens[index + 1].isdigit():
                results.append(spaced)
            elif any(spaced.startswith(prefix) for prefix in known_prefixes):
                results.append(spaced)
        return results

    @staticmethod
    def _first_or_none(items: List[str]) -> str | None:
        return items[0] if items else None
