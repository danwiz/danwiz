"""Command-line interface for scoring and reporting."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from report import generate_markdown_report
from scorer import load_json, score_assessment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="witrt", description="Wisdom IT Readiness Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    score_parser = subparsers.add_parser("score", help="Score an assessment and print JSON")
    score_parser.add_argument("assessment")
    score_parser.add_argument("responses")

    report_parser = subparsers.add_parser("report", help="Generate a Markdown readiness report")
    report_parser.add_argument("assessment")
    report_parser.add_argument("responses")
    report_parser.add_argument("--subject", default="Assessment subject")
    report_parser.add_argument("--data-note", default="User-provided assessment responses")
    report_parser.add_argument("--output", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    assessment = load_json(args.assessment)
    responses = load_json(args.responses)
    result = score_assessment(assessment, responses)

    if args.command == "score":
        print(json.dumps(result.__dict__, indent=2, sort_keys=True))
        return

    report = generate_markdown_report(
        assessment,
        result,
        subject=args.subject,
        data_note=args.data_note,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
