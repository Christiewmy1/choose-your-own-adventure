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


@dataclass
class TargetContext:
    name: str
    domain_focus: str
    target_skills: List[str]
    mapped_courses: List[str]
    notes: str = ""


class HuskyAdvisorEngine:
    def __init__(
        self,
        majors: Iterable[MajorRecord],
        courses: Iterable[CourseRecord],
        companies: Iterable[CompanyRecord],
        recent_offerings: dict[str, list[str]] | None = None,
        company_course_mapping: dict[str, list[str]] | None = None,
        company_intent_profiles: list[dict] | None = None,
        internship_playbooks: list[dict] | None = None,
        quarter_plan_templates: list[dict] | None = None,
    ) -> None:
        self.majors = list(majors)
        self.courses = list(courses)
        self.companies = list(companies)
        self.recent_offerings = recent_offerings or {}
        self.company_course_mapping = company_course_mapping or {}
        self.company_intent_profiles = company_intent_profiles or []
        self.internship_playbooks = internship_playbooks or []
        self.quarter_plan_templates = quarter_plan_templates or []
        self.major_alias_map = self._build_major_alias_map()
        self.major_anchor_courses = self._build_major_anchor_course_map()

    def recommend_electives(self, profile: StudentProfile, target_company: str | None = None) -> AdvisingResult:
        scope_result = self._scope_guard_result(
            profile,
            "Course Recommendation Scope Warning",
            "HuskyAdvisor cannot give a trustworthy course recommendation for this exact profile yet.",
        )
        if scope_result:
            return scope_result

        canonical_major = self._canonical_major(profile.major)
        target = self._resolve_target_context(target_company or self._first_or_none(profile.target_companies))
        scored = self._score_elective_courses(profile, target)
        top_courses = scored[:3]
        level_label = self._recommendation_level_label(profile)

        recommendations = [
            f"{item.course.course_code} {item.course.title}: {item.course.description}" for item in top_courses
        ]
        evidence = [reason for item in top_courses for reason in item.evidence[:2]]
        cautions = [
            f"Check prerequisites for {item.course.course_code}: {item.course.prerequisite_text}."
            for item in top_courses
        ]

        summary = (
            f"For a {profile.class_standing} {canonical_major} student targeting "
            f"{target.name if target else 'local technical roles'}, these next-step electives best balance fit,"
            " realism, and preparation value."
        )

        return AdvisingResult(
            title=f"Recommended {level_label} Courses",
            summary=summary,
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def recommend_companies(self, profile: StudentProfile) -> AdvisingResult:
        scope_result = self._scope_guard_result(
            profile,
            "Company Alignment Scope Warning",
            "HuskyAdvisor cannot give a trustworthy company-alignment result for this exact profile yet.",
        )
        if scope_result:
            return scope_result

        ranked: list[tuple[int, CompanyRecord, list[str]]] = []
        canonical_major = self._canonical_major(profile.major)
        resolved_targets = self._resolved_target_names(profile)
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
                if canonical_major in course.major_tags
                and self._overlap(course.career_tags, company.target_skills)
            ]
            if relevant_courses:
                score += min(3, len(relevant_courses))
                evidence.append(
                    f"Your program already connects to {company.name} through courses like {', '.join(relevant_courses[:3])}."
                )

            if company.name in resolved_targets:
                score += 2
                evidence.append(f"{company.name} is already one of your stated or inferred target companies.")

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
        scope_result = self._scope_guard_result(
            profile,
            "Internship Prep Scope Warning",
            "HuskyAdvisor cannot give a trustworthy internship-prep plan for this exact profile yet.",
        )
        if scope_result:
            return scope_result

        selected, selection_reasons = self._select_internship_playbook(profile)

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
        selected_track = selected.get("track", "general").replace("_", " ")
        next_actions = self._internship_next_actions(profile)

        recommendations = [
            f"Recommended next courses{target_hint}: {', '.join(remaining_courses)}",
            *next_project,
            *next_actions,
        ]
        evidence = [
            f"Chosen prep track: {selected_track}.",
            f"Target companies in this playbook: {', '.join(target_companies)}.",
            f"Suggested skills to strengthen: {', '.join(next_skills)}.",
            f"Completed courses already considered: {', '.join(profile.completed_courses) or 'none listed'}.",
            *selection_reasons[:2],
        ]
        cautions = [
            "This is a preparation guide, not a live internship feed.",
            "Use this together with current job boards and official internship postings.",
        ]
        return AdvisingResult(
            title="Internship Prep Plan",
            summary="This plan highlights the remaining courses, projects, and concrete next actions that best fit one likely internship pathway for your profile.",
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
        scope_result = self._scope_guard_result(
            profile,
            "Roadmap Scope Warning",
            "HuskyAdvisor cannot build a believable quarter-by-quarter roadmap for this exact profile yet.",
        )
        if scope_result:
            return scope_result

        selected_template = self._select_quarter_template(profile)
        completed = self._completed_course_set(profile)
        used_codes: set[str] = set()
        if selected_template:
            replacement_pool = [
                item.course.course_code
                for item in self._score_elective_courses(
                    profile,
                    self._resolve_target_context(self._first_or_none(profile.target_companies)),
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
        target: TargetContext | None = None,
    ) -> List[ScoredCourse]:
        scored: List[ScoredCourse] = []
        completed = self._completed_course_set(profile)
        canonical_major = self._canonical_major(profile.major)
        min_level, max_level = self._target_level_range(profile)

        for course in self.courses:
            if course.level < min_level or course.level > max_level:
                continue
            if self._normalize_code(course.course_code) in completed:
                continue

            score = 0
            evidence: List[str] = []

            if canonical_major in course.major_tags:
                score += 3
                evidence.append(f"{course.course_code} is tagged for {canonical_major}.")

            anchor_courses = self.major_anchor_courses.get(canonical_major, set())
            if course.course_code in anchor_courses:
                score += 2
                evidence.append(f"{course.course_code} is one of HuskyAdvisor's anchor courses for {canonical_major}.")

            score += self._quality_score_adjustment(course, evidence)

            recent_terms = self.recent_offerings.get(course.course_code, [])
            if recent_terms:
                score += 1
                evidence.append(
                    f"{course.course_code} appeared in recent terms: {', '.join(recent_terms)}."
                )

            if target:
                mapped_courses = target.mapped_courses
                if course.course_code in mapped_courses:
                    score += 2
                    evidence.append(f"{course.course_code} is explicitly mapped to {target.name} in the career dataset.")

                shared_skills = self._overlap(course.career_tags, target.target_skills)
                if shared_skills:
                    score += 2 * len(shared_skills)
                    evidence.append(
                        f"{course.course_code} overlaps with {target.name} skills: {', '.join(shared_skills)}."
                    )

                if "aerospace" in course.career_tags and "aerospace" in target.domain_focus.lower():
                    score += 2
                    evidence.append(f"{course.course_code} directly aligns with aerospace-oriented work.")
                if "privacy" in target.target_skills and "security" in course.career_tags:
                    score += 1
                    evidence.append(f"{course.course_code} supports privacy-aware and secure system work relevant to {target.name}.")
                if "data" in target.target_skills and "data" in course.career_tags:
                    score += 1
                    evidence.append(f"{course.course_code} supports data-centric work relevant to {target.name}.")

            goal_overlap = self._overlap(course.career_tags, profile.career_goals)
            if goal_overlap:
                score += len(goal_overlap)
                evidence.append(f"It supports your stated goals: {', '.join(goal_overlap)}.")

            if self._canonical_major(profile.major) == "EE":
                ee_focus = {"embedded", "hardware", "aerospace", "robotics", "systems"}
                if ee_focus.intersection({goal.lower() for goal in profile.career_goals}) and (
                    course.department == "EE" or "embedded" in course.career_tags or "hardware" in course.career_tags
                ):
                    score += 2
                    evidence.append("This course keeps your recommendations grounded in an EE-oriented pathway.")
            elif self._canonical_major(profile.major) == "Computer Engineering":
                if course.department == "EE" or {"embedded", "hardware", "systems"}.intersection(
                    {tag.lower() for tag in course.career_tags}
                ):
                    score += 2
                    evidence.append("This course reinforces the hardware-software bridge that Computer Engineering students usually need.")
            elif self._canonical_major(profile.major) == "Data Visualization":
                if {"data", "analytics", "dashboards", "machine learning"}.intersection(
                    {tag.lower() for tag in course.career_tags}
                ) or course.department in {"BIS", "STMATH"}:
                    score += 2
                    evidence.append("This course supports data analysis, visualization, or quantitative storytelling work.")
                if course.course_code.startswith(("BIS ", "STMATH ")):
                    score += 1
                    evidence.append("This course sits close to the analytics and quantitative core of Data Visualization.")
            elif self._canonical_major(profile.major) == "Business Administration":
                if course.department in {"BIS", "B BUS"} or {"analytics", "product", "business systems", "enterprise systems"}.intersection(
                    {tag.lower() for tag in course.career_tags}
                ):
                    score += 2
                    evidence.append("This course fits the technology-facing Business Administration pathways HuskyAdvisor currently models.")
                if course.course_code.startswith(("BIS ", "B BUS ")):
                    score += 3
                    evidence.append("This course is part of the MIS, analytics, or communication backbone for supported business-tech pathways.")

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

        standing_band = self._standing_band(profile)
        if standing_band == "early" and course.level >= 400:
            adjustment -= 4
            evidence.append("At your current stage, this looks more like a future target than an immediate next course.")
        elif standing_band == "mid" and course.level >= 480:
            adjustment -= 1
            evidence.append("This course may fit better after a bit more upper-division progress.")
        elif standing_band == "late" and course.level < 400:
            adjustment -= 1
            evidence.append("You may be ready to prioritize more advanced courses than this one.")

        if self._canonical_major(profile.major) == "EE" and course.department == "EE":
            adjustment += 1
            evidence.append("This EE course is especially relevant for your program background.")

        return adjustment

    def _canonical_major(self, value: str) -> str:
        lowered = value.strip().lower()
        if lowered in self.major_alias_map:
            return self.major_alias_map[lowered]
        if lowered in {"csse", "computer science and software engineering", "computer science & software engineering"}:
            return "CSSE"
        if lowered in {"applied computing", "ac"}:
            return "Applied Computing"
        if lowered in {"ee", "electrical engineering"}:
            return "EE"
        return value.strip()

    def _standing_band(self, profile: StudentProfile) -> str:
        standing = profile.class_standing.strip().lower()
        credits = profile.completed_credits
        if standing == "freshman" or credits < 45:
            return "early"
        if standing == "sophomore" or credits < 90:
            return "mid"
        if standing in {"junior", "senior", "graduate"} or credits >= 90:
            return "late"
        return "mid"

    def _target_level_range(self, profile: StudentProfile) -> tuple[int, int]:
        band = self._standing_band(profile)
        canonical_major = self._canonical_major(profile.major)
        if band == "early":
            return (200, 399)
        if band == "mid":
            return (300, 499)
        if canonical_major in {"EE", "Computer Engineering", "Data Visualization", "Business Administration"}:
            return (300, 499)
        return (400, 499)

    def _recommendation_level_label(self, profile: StudentProfile) -> str:
        band = self._standing_band(profile)
        if band == "early":
            return "Foundation and 300-Level Preparation"
        if band == "mid":
            return "300- and 400-Level Next-Step"
        return "Upper-Level"

    def _scope_guard_result(
        self,
        profile: StudentProfile,
        title: str,
        summary: str,
    ) -> AdvisingResult | None:
        issues = self._profile_scope_issues(profile)
        if not issues:
            return None

        supported_major_names = ", ".join(major.major_name for major in self.majors)
        recommendations = [
            f"Use one of the currently supported majors: {supported_major_names}.",
            "Use UWB-style course history when possible, such as CSS, EE, BIS, business, or related math courses already completed.",
            "Use one of the current company targets in the dataset, such as Boeing, Microsoft Redmond, T-Mobile, Amazon Bellevue, or Google Kirkland.",
        ]
        evidence = [
            "HuskyAdvisor is currently built around UW Bothell course and career pathways, not all UW majors or all employers.",
            *issues,
        ]
        cautions = [
            "Showing a generic recommendation here would be misleading, so HuskyAdvisor is intentionally warning instead.",
        ]
        return AdvisingResult(
            title=title,
            summary=summary,
            recommendations=recommendations,
            evidence=evidence,
            cautions=cautions,
        )

    def _profile_scope_issues(self, profile: StudentProfile) -> list[str]:
        issues: list[str] = []
        canonical_major = self._canonical_major(profile.major)
        supported_majors = {major.major_name for major in self.majors}
        if canonical_major not in supported_majors:
            issues.append(
                f"The major '{profile.major}' is outside the current supported UWB pathways in this prototype."
            )

        recognized_course_prefixes = ("CSS", "EE", "B EE", "BIS", "STMATH", "MATH", "B BUS")
        recognized_completed = [
            code
            for code in self._completed_course_set(profile)
            if any(code.startswith(prefix) for prefix in recognized_course_prefixes)
        ]
        if profile.completed_courses and not recognized_completed:
            issues.append(
                "The completed-course history does not match the UWB course families currently modeled in HuskyAdvisor."
            )

        if profile.target_companies:
            matched_companies = [company for company in profile.target_companies if self._resolve_target_context(company)]
            if not matched_companies:
                issues.append(
                    "The target company/field is not in the current local-company dataset, so company alignment would be guessy."
                )

        return issues

    def _resolved_target_names(self, profile: StudentProfile) -> set[str]:
        names: set[str] = set()
        for company in profile.target_companies:
            context = self._resolve_target_context(company)
            if context:
                names.add(context.name)
        return names

    def _resolve_target_context(self, name: str | None) -> TargetContext | None:
        if not name:
            return None

        exact_company = self._find_company(name)
        if exact_company:
            return TargetContext(
                name=exact_company.name,
                domain_focus=exact_company.domain_focus,
                target_skills=exact_company.target_skills,
                mapped_courses=self.company_course_mapping.get(exact_company.name, []),
                notes=exact_company.notes,
            )

        lowered = name.lower().strip()
        for profile in self.company_intent_profiles:
            aliases = [alias.lower() for alias in profile.get("aliases", [])]
            canonical_name = profile.get("canonical_name", "")
            if lowered == canonical_name.lower() or lowered in aliases:
                return TargetContext(
                    name=canonical_name,
                    domain_focus=profile.get("domain_focus", ""),
                    target_skills=profile.get("target_skills", []),
                    mapped_courses=[self._normalize_code(code) for code in profile.get("recommended_courses", [])],
                    notes="Resolved through company intent profile.",
                )

            alias_tokens = " ".join(aliases)
            if lowered and lowered in alias_tokens:
                return TargetContext(
                    name=canonical_name,
                    domain_focus=profile.get("domain_focus", ""),
                    target_skills=profile.get("target_skills", []),
                    mapped_courses=[self._normalize_code(code) for code in profile.get("recommended_courses", [])],
                    notes="Resolved through company intent profile.",
                )

        return None

    def _playbook_company_matches(self, playbook: dict, profile: StudentProfile) -> list[str]:
        targets = {name.lower() for name in self._resolved_target_names(profile)}
        return [
            company
            for company in playbook.get("target_companies", [])
            if company.lower() in targets
        ]

    def _template_company_match_score(self, template: dict, profile: StudentProfile) -> int:
        targets = {name.lower() for name in self._resolved_target_names(profile)}
        return sum(
            1
            for company in template.get("recommended_companies", [])
            if company.lower() in targets
        )

    def _template_major_bonus(self, template: dict, profile: StudentProfile) -> int:
        track = template.get("track", "")
        canonical_major = self._canonical_major(profile.major)
        if canonical_major == "EE" and track == "embedded_hardware":
            return 2
        if canonical_major == "Computer Engineering" and track in {"embedded_hardware", "systems_software"}:
            return 2
        if canonical_major == "Applied Computing" and track in {"cloud_platforms", "security_infrastructure"}:
            return 2
        if canonical_major == "Data Visualization" and track in {"cloud_platforms", "healthcare_data_platforms"}:
            return 2
        if canonical_major == "Business Administration" and track in {"cloud_platforms", "healthcare_data_platforms"}:
            return 1
        if canonical_major == "CSSE" and track == "systems_software":
            return 1
        return 0

    def _internship_next_actions(self, profile: StudentProfile) -> list[str]:
        standing = profile.class_standing.lower()
        if standing == "freshman":
            return [
                "Immediate next action: choose one starter project and one target skill to build before your first internship cycle."
            ]
        if standing == "sophomore":
            return [
                "Immediate next action: turn one class project into a resume bullet and start collecting internship-ready artifacts."
            ]
        return [
            "Immediate next action: tailor one portfolio project and one resume bullet directly to this pathway before applying."
        ]

    def _build_major_alias_map(self) -> dict[str, str]:
        alias_map: dict[str, str] = {}
        for major in self.majors:
            alias_map[major.major_name.strip().lower()] = major.major_name
            for alias in major.aliases:
                alias_map[alias.strip().lower()] = major.major_name
        return alias_map

    def _build_major_anchor_course_map(self) -> dict[str, set[str]]:
        anchor_map: dict[str, set[str]] = {}
        for major in self.majors:
            codes = set(major.typical_courses)
            for group_codes in major.course_groups.values():
                codes.update(group_codes)
            anchor_map[major.major_name] = {self._normalize_code(code) for code in codes}
        return anchor_map

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
            score = 3 * len(self._overlap(keywords, lowered_goals))
            score += 3 * self._template_company_match_score(template, profile)
            score += self._template_major_bonus(template, profile)
            if score > best_score:
                best_score = score
                best_template = template

        return best_template if best_score > 0 else self.quarter_plan_templates[0]

    def _select_internship_playbook(self, profile: StudentProfile) -> tuple[dict | None, list[str]]:
        if not self.internship_playbooks:
            return None, []

        lowered_goals = [goal.lower() for goal in profile.career_goals]
        completed = self._completed_course_set(profile)
        best_playbook: dict | None = None
        best_reasons: list[str] = []
        best_score = -1

        for playbook in self.internship_playbooks:
            score = 0
            reasons: list[str] = []
            keywords = [keyword.lower() for keyword in playbook.get("goal_keywords", [])]
            skills = [skill.lower() for skill in playbook.get("recommended_skills", [])]
            company_matches = self._playbook_company_matches(playbook, profile)

            goal_overlap = self._overlap(keywords or skills, lowered_goals)
            if goal_overlap:
                score += 3 * len(goal_overlap)
                reasons.append(f"Your goals overlap with this track through {', '.join(goal_overlap)}.")

            if company_matches:
                score += 4 * len(company_matches)
                reasons.append(f"This track directly matches your target companies through {', '.join(company_matches)}.")

            canonical_major = self._canonical_major(profile.major)
            if canonical_major in playbook.get("preferred_majors", []):
                score += 2
                reasons.append(f"This track is a natural fit for {canonical_major} students.")

            remaining_course_count = sum(
                1
                for code in playbook.get("recommended_courses", [])
                if self._normalize_code(code) not in completed
            )
            score += min(2, remaining_course_count)

            if score > best_score:
                best_score = score
                best_playbook = playbook
                best_reasons = reasons

        return best_playbook, best_reasons

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
        known_prefixes = ("CSS ", "EE ", "B EE ", "BIS ")
        tokens = prerequisite_text.replace(",", " ").split()
        results: List[str] = []
        for index, token in enumerate(tokens[:-1]):
            spaced = f"{token} {tokens[index + 1]}"
            if token in {"CSS", "EE", "BIS"} and tokens[index + 1].isdigit():
                results.append(spaced)
            elif token == "B" and index + 2 < len(tokens) and tokens[index + 1] == "EE" and tokens[index + 2].isdigit():
                results.append(f"B EE {tokens[index + 2]}")
            elif any(spaced.startswith(prefix) for prefix in known_prefixes):
                results.append(spaced)
        return results

    @staticmethod
    def _first_or_none(items: List[str]) -> str | None:
        return items[0] if items else None
