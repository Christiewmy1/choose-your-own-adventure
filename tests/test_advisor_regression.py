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


if __name__ == "__main__":
    unittest.main()
