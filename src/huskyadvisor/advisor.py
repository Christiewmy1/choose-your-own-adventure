from __future__ import annotations

from dataclasses import dataclass
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
    ) -> None:
        self.majors = list(majors)
        self.courses = list(courses)
        self.companies = list(companies)

    def recommend_electives(self, profile: StudentProfile, target_company: str | None = None) -> AdvisingResult:
        company = self._find_company(target_company or self._first_or_none(profile.target_companies))
        scored: List[ScoredCourse] = []

        for course in self.courses:
            if course.level < 400:
                continue

            score = 0
            evidence: List[str] = []

            if profile.major in course.major_tags:
                score += 3
                evidence.append(f"{course.course_code} is tagged for {profile.major}.")

            if company:
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

            completed = set(profile.completed_courses)
            prereq_ready = all(token in completed for token in self._extract_prereq_courses(course.prerequisite_text))
            if prereq_ready:
                score += 1
                evidence.append("Your completed courses suggest you are reasonably prepared.")
            else:
                evidence.append("You may need to verify prerequisites before enrolling.")

            scored.append(ScoredCourse(course=course, score=score, evidence=evidence))

        scored.sort(key=lambda item: item.score, reverse=True)
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
            f"{company.name if company else 'local technical roles'}, these courses best match systems,"
            " aerospace, and reliable software preparation."
        )

        return AdvisingResult(
            title="Recommended 400-Level Electives",
            summary=summary,
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
        next_steps = [
            "Quarter 1: Take one systems-oriented elective and build a small class-aligned project with tests.",
            "Quarter 2: Strengthen teamwork experience through a larger software project and resume-ready documentation.",
            "Quarter 3: Tailor a project toward your target industry, such as aerospace reliability or embedded software.",
        ]
        evidence = [
            f"You already completed: {', '.join(profile.completed_courses)}.",
            f"Your target companies include: {', '.join(profile.target_companies) or 'regional employers'}.",
        ]
        cautions = [
            "Confirm prerequisite sequencing with an advisor before treating this as an official degree plan.",
        ]
        return AdvisingResult(
            title="Quarter-by-Quarter Success Roadmap",
            summary="This roadmap focuses on building internship-ready systems experience without overloading the MVP.",
            recommendations=next_steps,
            evidence=evidence,
            cautions=cautions,
        )

    def _find_company(self, name: str | None) -> CompanyRecord | None:
        if not name:
            return None
        lowered = name.lower()
        for company in self.companies:
            if company.name.lower() == lowered:
                return company
        return None

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
