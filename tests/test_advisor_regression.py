from __future__ import annotations

import unittest

from huskyadvisor.service import build_json_advisor
from huskyadvisor.models import StudentProfile


class AdvisorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.advisor = build_json_advisor()

    def test_completed_courses_are_not_recommended_even_with_messy_input(self) -> None:
        profile = StudentProfile(
            student_id="regression-1",
            name="Regression Student",
            major="CSSE",
            class_standing="Junior",
            gpa=3.2,
            completed_credits=100,
            completed_courses=["I already took CSS 430 and CSS 458", "css427"],
            preferred_learning_style="project-based",
            career_goals=["systems", "embedded"],
            target_companies=["Boeing"],
            internship_timeline="next summer",
        )

        result = self.advisor.recommend_electives(profile, "Boeing")
        joined = " ".join(result.recommendations)
        self.assertNotIn("CSS 430", joined)
        self.assertNotIn("CSS 458", joined)
        self.assertNotIn("CSS 427", joined)

    def test_roadmap_replaces_completed_template_courses(self) -> None:
        profile = StudentProfile(
            student_id="regression-2",
            name="Roadmap Student",
            major="CSSE",
            class_standing="Junior",
            gpa=3.4,
            completed_credits=95,
            completed_courses=["CSS 430"],
            preferred_learning_style="project-based",
            career_goals=["systems", "software engineering"],
            target_companies=["Boeing"],
            internship_timeline="next summer",
        )

        result = self.advisor.build_quarter_plan(profile)
        joined = " ".join(result.recommendations)
        self.assertNotIn("Suggested courses: CSS 430", joined)
        self.assertIn("Completed courses were removed from the roadmap", " ".join(result.evidence))

    def test_placeholder_catalog_entries_do_not_dominate_cloud_profile(self) -> None:
        profile = StudentProfile(
            student_id="regression-3",
            name="Cloud Student",
            major="Applied Computing",
            class_standing="Sophomore",
            gpa=3.1,
            completed_credits=60,
            completed_courses=["CSS 142", "CSS 143", "CSS 301"],
            preferred_learning_style="hands-on",
            career_goals=["web development", "cloud", "software engineering"],
            target_companies=["Microsoft Redmond"],
            internship_timeline="next year",
        )

        result = self.advisor.recommend_electives(profile, "Microsoft Redmond")
        self.assertTrue(result.recommendations)
        self.assertNotIn("Catalog-derived placeholder", result.recommendations[0])

    def test_freshman_gets_foundational_or_mid_level_path_not_400_only(self) -> None:
        profile = StudentProfile(
            student_id="regression-4",
            name="Freshman Student",
            major="CSSE",
            class_standing="Freshman",
            gpa=3.0,
            completed_credits=20,
            completed_courses=["CSS 101"],
            preferred_learning_style="project-based",
            career_goals=["software engineering", "cloud"],
            target_companies=[],
            internship_timeline="later",
        )

        result = self.advisor.recommend_electives(profile)
        self.assertIn("Foundation and 300-Level Preparation", result.title)
        self.assertTrue(result.recommendations)

    def test_major_alias_is_normalized_for_ee_students(self) -> None:
        profile = StudentProfile(
            student_id="regression-5",
            name="EE Student",
            major="Electrical Engineering",
            class_standing="Senior",
            gpa=3.5,
            completed_credits=130,
            completed_courses=["EE 215", "EE 233"],
            preferred_learning_style="lab-based",
            career_goals=["embedded", "hardware", "aerospace"],
            target_companies=["Boeing"],
            internship_timeline="this year",
        )

        result = self.advisor.recommend_electives(profile, "Boeing")
        self.assertTrue(result.recommendations)
        joined = " ".join(result.recommendations)
        self.assertTrue("EE " in joined or "CSS 422" in joined or "CSS 427" in joined)

    def test_tmobile_security_student_gets_security_prep_track(self) -> None:
        profile = StudentProfile(
            student_id="regression-6",
            name="Security Student",
            major="CSSE",
            class_standing="Sophomore",
            gpa=3.1,
            completed_credits=60,
            completed_courses=["CSS 142", "CSS 143"],
            preferred_learning_style="project-based",
            career_goals=["security", "cloud", "systems"],
            target_companies=["T-Mobile"],
            internship_timeline="next summer",
        )

        internship = self.advisor.recommend_internship_prep(profile)
        roadmap = self.advisor.build_quarter_plan(profile)
        self.assertIn("security infrastructure", " ".join(internship.evidence))
        self.assertIn("CSS 310", " ".join(internship.recommendations))
        self.assertIn("CSS 310", " ".join(roadmap.recommendations))

    def test_cloud_student_gets_cloud_playbook_instead_of_generic_systems(self) -> None:
        profile = StudentProfile(
            student_id="regression-7",
            name="Cloud Student 2",
            major="Applied Computing",
            class_standing="Junior",
            gpa=3.3,
            completed_credits=95,
            completed_courses=["CSS 142", "CSS 143", "CSS 301", "CSS 370"],
            preferred_learning_style="project-based",
            career_goals=["web development", "cloud", "software engineering"],
            target_companies=["Microsoft Redmond"],
            internship_timeline="next summer",
        )

        internship = self.advisor.recommend_internship_prep(profile)
        roadmap = self.advisor.build_quarter_plan(profile)
        self.assertIn("cloud backend", " ".join(internship.evidence))
        self.assertIn("CSS 436", " ".join(internship.recommendations))
        self.assertIn("cloud_platforms", " ".join(roadmap.evidence))

    def test_out_of_scope_profile_gets_honest_warning_instead_of_fake_personalization(self) -> None:
        profile = StudentProfile(
            student_id="regression-8",
            name="Out of Scope Student",
            major="Informatics",
            class_standing="Freshman",
            gpa=3.2,
            completed_credits=20,
            completed_courses=["INFO 200"],
            preferred_learning_style="project-based",
            career_goals=["cloud"],
            target_companies=["UW Hospital"],
            internship_timeline="later",
        )

        result = self.advisor.recommend_electives(profile)
        joined = " ".join(result.evidence + result.cautions + result.recommendations)
        self.assertIn("outside the current supported UWB pathways", joined)
        self.assertIn("misleading", joined.lower())

    def test_supported_major_with_uw_hospital_target_resolves_to_healthcare_pathway(self) -> None:
        profile = StudentProfile(
            student_id="regression-9",
            name="Healthcare Student",
            major="Applied Computing",
            class_standing="Junior",
            gpa=3.3,
            completed_credits=95,
            completed_courses=["CSS 142", "CSS 143", "CSS 301", "CSS 370"],
            preferred_learning_style="project-based",
            career_goals=["cloud", "data", "privacy"],
            target_companies=["UW Hospital"],
            internship_timeline="next summer",
        )

        electives = self.advisor.recommend_electives(profile, "UW Hospital")
        companies = self.advisor.recommend_companies(profile)
        internship = self.advisor.recommend_internship_prep(profile)
        roadmap = self.advisor.build_quarter_plan(profile)

        self.assertNotIn("Scope Warning", electives.title)
        self.assertIn("UW Medicine", " ".join(companies.recommendations + companies.evidence))
        self.assertIn("healthcare digital", " ".join(internship.evidence).lower())
        self.assertIn("healthcare_data_platforms", " ".join(roadmap.evidence))


if __name__ == "__main__":
    unittest.main()
