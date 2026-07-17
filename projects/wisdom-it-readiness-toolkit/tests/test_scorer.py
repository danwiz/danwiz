import unittest

from projects.wisdom_it_readiness_toolkit.src.scorer import score_assessment


ASSESSMENT = {
    "domains": [
        {
            "id": "strategy",
            "questions": [
                {"id": "strategy-1"},
                {"id": "strategy-2"},
            ],
        },
        {
            "id": "security",
            "questions": [
                {"id": "security-1"},
                {"id": "security-2"},
            ],
        },
    ]
}


class ScoreAssessmentTests(unittest.TestCase):
    def test_scores_complete_assessment(self):
        result = score_assessment(
            ASSESSMENT,
            {
                "strategy-1": 3,
                "strategy-2": 4,
                "security-1": 2,
                "security-2": 3,
            },
        )

        self.assertEqual(result.domain_scores, {"strategy": 3.5, "security": 2.5})
        self.assertEqual(result.overall_score, 3.0)
        self.assertEqual(result.maturity_level, 3)
        self.assertEqual(result.maturity_label, "Repeatable")
        self.assertEqual(result.unanswered_questions, [])

    def test_reports_missing_responses(self):
        result = score_assessment(ASSESSMENT, {"strategy-1": 5})
        self.assertEqual(result.domain_scores, {"strategy": 5.0})
        self.assertEqual(
            result.unanswered_questions,
            ["strategy-2", "security-1", "security-2"],
        )

    def test_rejects_out_of_range_response(self):
        with self.assertRaises(ValueError):
            score_assessment(ASSESSMENT, {"strategy-1": 6})

    def test_rejects_empty_response_set(self):
        with self.assertRaises(ValueError):
            score_assessment(ASSESSMENT, {})


if __name__ == "__main__":
    unittest.main()
