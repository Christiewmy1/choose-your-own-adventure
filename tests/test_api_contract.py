from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from api.main import app


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.profile_payload = {
            "major": "Computer Science and Software Engineering",
            "class_standing": "Junior",
            "completed_courses": ["CSS 142", "CSS 143", "CSS 301"],
            "career_goals": ["cloud", "software engineering"],
            "target_companies": ["Microsoft Redmond"],
        }

    def assert_valid_result(self, payload: dict) -> None:
        for key in ["title", "summary", "recommendations", "evidence", "cautions", "ai_trace"]:
            self.assertIn(key, payload)
        self.assertIsInstance(payload["recommendations"], list)
        self.assertTrue(payload["recommendations"])
        self.assertIsInstance(payload["evidence"], list)
        self.assertIsInstance(payload["cautions"], list)
        trace = payload["ai_trace"]
        self.assertIn("structured scoring", trace["recommendation_engine"])
        self.assertIn("Crawl4AI", trace["data_ingestion"])
        self.assertIsInstance(trace["fallback_mode"], bool)
        self.assertIsInstance(trace["decision_inputs"], list)
        self.assertTrue(trace["decision_inputs"])

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["api_contract"], "ai_trace_v1")
        self.assertGreaterEqual(payload["supported_major_pathways"], 6)
        self.assertGreaterEqual(payload["course_records"], 120)
        self.assertGreaterEqual(payload["company_records"], 140)

    def test_profile_dashboard_endpoints_return_contract_shape(self) -> None:
        for path in [
            "/api/profile/recommendations",
            "/api/profile/companies",
            "/api/profile/internship-prep",
            "/api/profile/roadmap",
            "/api/profile/major",
        ]:
            with self.subTest(path=path):
                response = self.client.post(path, json=self.profile_payload)
                self.assertEqual(response.status_code, 200)
                self.assert_valid_result(response.json())

    def test_getting_post_only_recommendation_route_is_explicitly_not_allowed(self) -> None:
        response = self.client.get("/api/profile/recommendations")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
