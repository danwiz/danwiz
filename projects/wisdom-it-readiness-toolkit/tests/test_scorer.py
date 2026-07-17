import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from scorer import score_assessment  # noqa: E402

ASSESSMENT = {
    "scale": {"0": "No", "1": "Partial", "2": "Yes"},
    "domains": [
        {"id": "strategy", "questions": [{"id": "s1", "weight": 2}, {"id": "s2", "weight": 1}]},
        {"id": "security", "questions": [{"id": "c1", "weight": 3}, {"id": "c2", "weight": 1}]},
    ],
    "maturity_bands": [
        {"minimum_percent": 0, "maximum_percent": 24, "level": 1, "label": "Unprepared"},
        {"minimum_percent": 25, "maximum_percent": 44, "level": 2, "label": "Basic"},
        {"minimum_percent": 45, "maximum_percent": 64, "level": 3, "label": "Repeatable"},
        {"minimum_percent": 65, "maximum_percent": 84, "level": 4, "label": "Managed"},
        {"minimum_percent": 85, "maximum_percent": 100, "level": 5, "label": "Optimized"},
    ],
}


class ScoreAssessmentTests(unittest.TestCase):
    def test_scores_complete_assessment(self):
        result = score_assessment(ASSESSMENT, {"s1": 2, "s2": 1, "c1": 1, "c2": 2})
        self.assertEqual(result.domain_scores, {"strategy": 83.33, "security": 62.5})
        self.assertEqual(result.overall_percent, 71.43)
        self.assertEqual(result.maturity_label, "Managed")
        self.assertEqual(result.unanswered_questions, [])

    def test_reports_missing_responses(self):
        result = score_assessment(ASSESSMENT, {"s1": 2})
        self.assertEqual(result.domain_scores, {"strategy": 100.0})
        self.assertEqual(result.unanswered_questions, ["s2", "c1", "c2"])

    def test_rejects_out_of_range_response(self):
        with self.assertRaises(ValueError):
            score_assessment(ASSESSMENT, {"s1": 3})

    def test_rejects_empty_response_set(self):
        with self.assertRaises(ValueError):
            score_assessment(ASSESSMENT, {})


if __name__ == "__main__":
    unittest.main()
