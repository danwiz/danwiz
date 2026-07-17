import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from report import generate_markdown_report  # noqa: E402
from scorer import ScoreResult  # noqa: E402


ASSESSMENT = {
    "assessment_id": "WITRT-TEST-001",
    "title": "Technology Readiness Quick Check",
    "version": "0.1.0",
    "domains": [
        {"id": "strategy", "title": "Strategy and Goals", "questions": [{"id": "STR-01"}]},
        {"id": "security", "title": "Cybersecurity", "questions": [{"id": "SEC-01"}]},
    ],
}


class MarkdownReportTests(unittest.TestCase):
    def test_generates_expected_sections(self):
        result = ScoreResult(
            overall_score=50.0,
            maturity_level=3,
            maturity_label="Repeatable",
            domain_scores={"strategy": 75.0, "security": 25.0},
            unanswered_questions=[],
        )
        report = generate_markdown_report(ASSESSMENT, result, subject="Synthetic Example")

        self.assertIn("# Technology Readiness Quick Check — Report", report)
        self.assertIn("**Subject:** Synthetic Example", report)
        self.assertIn("**Overall score:** 50.00%", report)
        self.assertIn("- Strategy and Goals: 75.00%", report)
        self.assertIn("- Cybersecurity: 25.00%", report)
        self.assertIn("## Priority actions", report)

    def test_lists_incomplete_responses(self):
        result = ScoreResult(
            overall_score=75.0,
            maturity_level=4,
            maturity_label="Managed",
            domain_scores={"strategy": 75.0},
            unanswered_questions=["SEC-01"],
        )
        report = generate_markdown_report(ASSESSMENT, result)
        self.assertIn("## Incomplete responses", report)
        self.assertIn("- SEC-01", report)


if __name__ == "__main__":
    unittest.main()
