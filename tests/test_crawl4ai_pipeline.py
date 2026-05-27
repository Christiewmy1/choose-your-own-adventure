from __future__ import annotations

import unittest

from huskyadvisor.crawl4ai_pipeline import (
    build_retrieval_document,
    build_summary_record,
    extract_course_codes,
    infer_page_type,
    slugify_target,
)


class Crawl4AIPipelineTests(unittest.TestCase):
    def test_slugify_target_prefers_label_when_present(self) -> None:
        self.assertEqual(
            slugify_target("https://www.uwb.edu/stem/undergraduate/majors/csse", "UWB CSSE"),
            "uwb-csse",
        )

    def test_extract_course_codes_normalizes_spacing(self) -> None:
        codes = extract_course_codes("css430 and B EE 233 are both mentioned", "Take CSS  457 next")
        self.assertEqual(codes, ["CSS 430", "CSS 457", "EE 233"])

    def test_infer_page_type_uses_tags_first(self) -> None:
        self.assertEqual(infer_page_type(["company", "careers"], "https://example.com/jobs", "Jobs"), "company")
        self.assertEqual(infer_page_type(["schedule"], "https://example.com/timeschd", "Schedule"), "schedule")

    def test_build_summary_record_extracts_useful_metadata(self) -> None:
        payload = {
            "target_id": "uwb-css-page",
            "label": "UWB CSS schedule",
            "url": "https://www.washington.edu/students/timeschd/pub/B/SPR2026/css.html",
            "tags": ["uwb", "schedule", "css"],
            "title": "CSS Spring 2026",
            "markdown": "CSS 430 Software Engineering meets on MW. CSS 457 Security is also offered.",
            "captured_at": "2026-05-26T00:00:00Z",
            "crawl_metadata": {"success": True},
        }
        summary = build_summary_record(payload)
        self.assertEqual(summary["page_type"], "schedule")
        self.assertEqual(summary["course_codes"], ["CSS 430", "CSS 457"])
        self.assertGreater(summary["word_count"], 0)

    def test_build_retrieval_document_truncates_and_keeps_course_codes(self) -> None:
        payload = {
            "target_id": "microsoft-careers",
            "label": "Microsoft careers",
            "url": "https://careers.microsoft.com",
            "tags": ["company", "careers", "cloud"],
            "title": "Microsoft Careers",
            "markdown": "Cloud platform roles. " * 800,
        }
        document = build_retrieval_document(payload)
        self.assertEqual(document["page_type"], "company")
        self.assertLessEqual(len(document["content"]), 8000)

    def test_build_summary_record_handles_missing_title_and_metadata(self) -> None:
        payload = {
            "target_id": "untitled-page",
            "label": "Fallback label",
            "url": "https://example.com/reference",
            "tags": [],
            "markdown": "General reference page without course codes.",
        }
        summary = build_summary_record(payload)
        self.assertEqual(summary["title"], "Untitled page")
        self.assertEqual(summary["page_type"], "reference")
        self.assertEqual(summary["course_codes"], [])

    def test_company_page_does_not_get_misclassified_as_course_page(self) -> None:
        payload = {
            "target_id": "healthcare-company",
            "label": "UW Medicine About",
            "url": "https://www.uwmedicine.org/about",
            "tags": ["company", "healthcare", "privacy"],
            "title": "About UW Medicine",
            "markdown": "We build secure healthcare systems and privacy-aware data platforms.",
        }
        summary = build_summary_record(payload)
        self.assertEqual(summary["page_type"], "company")

    def test_retrieval_document_handles_empty_markdown(self) -> None:
        payload = {
            "target_id": "empty-page",
            "label": "Empty page",
            "url": "https://example.com/empty",
            "tags": ["reference"],
            "title": "Empty",
            "markdown": "",
        }
        document = build_retrieval_document(payload)
        self.assertEqual(document["content"], "")


if __name__ == "__main__":
    unittest.main()
