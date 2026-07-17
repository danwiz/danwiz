"""Markdown report generation for the Wisdom IT Readiness Toolkit."""

from __future__ import annotations

from typing import Any

from scorer import ScoreResult


def _domain_title_map(assessment: dict[str, Any]) -> dict[str, str]:
    return {
        str(domain["id"]): str(domain.get("title", domain["id"]))
        for domain in assessment.get("domains", [])
    }


def generate_markdown_report(
    assessment: dict[str, Any],
    result: ScoreResult,
    *,
    subject: str = "Assessment subject",
    data_note: str = "User-provided assessment responses",
) -> str:
    """Generate a concise executive Markdown readiness report."""
    titles = _domain_title_map(assessment)
    lines = [
        f"# {assessment.get('title', 'Technology Readiness Assessment')} — Report",
        "",
        f"**Subject:** {subject}  ",
        f"**Assessment:** {assessment.get('assessment_id', 'unknown')} v{assessment.get('version', 'unknown')}  ",
        f"**Data:** {data_note}  ",
        f"**Overall score:** {result.overall_score:.2f}%  ",
        f"**Maturity:** Level {result.maturity_level} — {result.maturity_label}",
        "",
        "## Domain results",
        "",
    ]

    for domain_id, score in result.domain_scores.items():
        lines.append(f"- {titles.get(domain_id, domain_id)}: {score:.2f}%")

    lines.extend(
        [
            "",
            "## Executive interpretation",
            "",
            _interpret(result),
            "",
            "## Priority actions",
            "",
        ]
    )

    for index, action in enumerate(_priority_actions(result), start=1):
        lines.append(f"{index}. {action}")

    lines.extend(
        [
            "",
            "## Evidence required for closure",
            "",
            "- Named owner and target date for each remediation action",
            "- Configuration, policy, checklist, or system evidence supporting closure",
            "- Verification record showing the control operates as intended",
            "- Updated risk and action registers",
        ]
    )

    if result.unanswered_questions:
        lines.extend(
            [
                "",
                "## Incomplete responses",
                "",
                *[f"- {question_id}" for question_id in result.unanswered_questions],
            ]
        )

    return "\n".join(lines) + "\n"


def _interpret(result: ScoreResult) -> str:
    if result.maturity_level == 1:
        return "Technology readiness is materially underdeveloped. Immediate stabilization and risk reduction should precede broader modernization."
    if result.maturity_level == 2:
        return "Basic capabilities exist, but they are inconsistent and depend heavily on informal practices. Priority controls should be standardized and verified."
    if result.maturity_level == 3:
        return "Core practices are becoming repeatable, but important weaknesses remain. The next step is to formalize ownership, evidence, and review cycles."
    if result.maturity_level == 4:
        return "Technology capabilities are generally managed and measurable. Improvement should focus on resilience, automation, and cross-domain optimization."
    return "Technology readiness is highly mature. Maintain assurance through continuous measurement, testing, and controlled improvement."


def _priority_actions(result: ScoreResult) -> list[str]:
    ordered = sorted(result.domain_scores.items(), key=lambda item: item[1])
    actions = [
        f"Create a remediation plan for the lowest-scoring domain: {domain_id} ({score:.2f}%)."
        for domain_id, score in ordered[:2]
    ]
    actions.extend(
        [
            "Assign accountable owners to all priority technology risks.",
            "Define evidence and acceptance criteria before marking actions complete.",
            "Repeat the assessment after remediation to measure improvement.",
        ]
    )
    return actions[:5]
