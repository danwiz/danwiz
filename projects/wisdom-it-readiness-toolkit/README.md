# Wisdom IT Readiness Toolkit

A governed open-source toolkit for assessing and improving practical technology readiness for individuals, founders, working professionals, and small businesses.

## MVP outcomes

The toolkit helps users:

- assess current technology readiness;
- identify operational, security, infrastructure, and digital-workplace gaps;
- calculate a transparent readiness score;
- prioritize remediation actions;
- generate a concise evidence-backed readiness report.

## Initial modules

1. Technology Readiness Quick Check
2. IT Environment Assessment
3. Cybersecurity Readiness Assessment
4. Digital Workspace Assessment
5. Scoring and Maturity Model
6. Evidence and Remediation Register
7. Example Reports

## Quick start

From `projects/wisdom-it-readiness-toolkit`:

```bash
python src/cli.py score \
  assessments/quick-check-v0.1.json \
  examples/synthetic-responses.json
```

Generate a Markdown report:

```bash
python src/cli.py report \
  assessments/quick-check-v0.1.json \
  examples/synthetic-responses.json \
  --subject "Synthetic Demonstration" \
  --data-note "Synthetic demonstration only" \
  --output build/example-report.md
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Output model

The scoring engine produces:

- overall readiness percentage;
- maturity level and label;
- per-domain readiness percentages;
- unanswered-question tracking;
- deterministic Markdown reporting.

## Delivery sequence

- Phase 0: Governance, schema, sample data, and acceptance criteria — complete
- Phase 1: Markdown and JSON assessment pack — complete
- Phase 2: Command-line interface and automated report generation — working MVP
- Phase 3: Lightweight web interface — planned
- Phase 4: Extensible integrations and reporting — planned

## Governance

This incubator is controlled by the Wisdom Technologies documentation taxonomy, secure-by-default repository standards, and the AI Governance baseline. It does not collect or transmit assessment data. Users remain responsible for protecting response files and generated reports.

A dedicated public repository will be promoted after the remaining release gates are met.

## Promotion gates

- CI passes on the current MVP
- Generated report artifact is verified
- Accessibility and documentation review is complete
- Dedicated repository is created
- Initial `v0.1.0` release is tagged

## Status

**Governed working MVP — promotion review in progress**
