"""Deterministic scoring for the Wisdom IT Readiness Toolkit."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LEVELS = {
    1: "Unprepared",
    2: "Basic",
    3: "Repeatable",
    4: "Managed",
    5: "Optimized",
}


@dataclass(frozen=True)
class ScoreResult:
    overall_score: float
    maturity_level: int
    maturity_label: str
    domain_scores: dict[str, float]
    unanswered_questions: list[str]


def _validate_score(value: Any, question_id: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Response for {question_id} must be an integer from 1 to 5")
    if value not in LEVELS:
        raise ValueError(f"Response for {question_id} must be between 1 and 5")
    return value


def score_assessment(assessment: dict[str, Any], responses: dict[str, Any]) -> ScoreResult:
    """Score a readiness assessment using equal domain and question weights.

    Missing responses are reported and excluded from averages. A completely
    unanswered assessment is rejected because it cannot produce a meaningful score.
    """
    domains = assessment.get("domains")
    if not isinstance(domains, list) or not domains:
        raise ValueError("Assessment must define at least one domain")

    domain_scores: dict[str, float] = {}
    unanswered: list[str] = []

    for domain in domains:
        domain_id = domain.get("id")
        questions = domain.get("questions", [])
        if not domain_id or not isinstance(questions, list) or not questions:
            raise ValueError("Every domain must have an id and at least one question")

        values: list[int] = []
        for question in questions:
            question_id = question.get("id")
            if not question_id:
                raise ValueError(f"Domain {domain_id} contains a question without an id")
            if question_id not in responses:
                unanswered.append(question_id)
                continue
            values.append(_validate_score(responses[question_id], question_id))

        if values:
            domain_scores[domain_id] = round(sum(values) / len(values), 2)

    if not domain_scores:
        raise ValueError("At least one valid response is required")

    overall = round(sum(domain_scores.values()) / len(domain_scores), 2)
    maturity_level = min(5, max(1, round(overall)))

    return ScoreResult(
        overall_score=overall,
        maturity_level=maturity_level,
        maturity_label=LEVELS[maturity_level],
        domain_scores=domain_scores,
        unanswered_questions=unanswered,
    )


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Score a Wisdom IT readiness assessment")
    parser.add_argument("assessment", help="Path to the assessment JSON file")
    parser.add_argument("responses", help="Path to the response JSON file")
    args = parser.parse_args()

    result = score_assessment(load_json(args.assessment), load_json(args.responses))
    print(json.dumps(result.__dict__, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
