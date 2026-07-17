# Wisdom IT Readiness Toolkit v0.1.0

## Release status

Release candidate prepared in the `danwiz/danwiz` incubator. Promotion to a dedicated repository and tagged release remains pending.

## Included

- Technology Readiness Quick Check assessment schema
- Deterministic weighted scoring engine
- Five-level maturity model
- Command-line `score` and `report` commands
- Markdown readiness report generation
- Synthetic demonstration responses
- Example readiness report
- Unit tests and CI smoke tests
- Security, contribution, accessibility, and data-dictionary documentation
- MIT license

## Example commands

```bash
python src/cli.py score assessments/quick-check-v0.1.json examples/synthetic-responses.json
```

```bash
python src/cli.py report assessments/quick-check-v0.1.json examples/synthetic-responses.json --output build/example-report.md
```

## Known limitations

- The project is not packaged for installation from PyPI.
- The web interface is not included.
- Report recommendations are template-based and require human review for client use.
- CI status must be verified in the dedicated repository after promotion.

## Promotion approval criteria

- Dedicated public repository created under `danwiz`.
- Incubator files migrated without history-sensitive secrets or private data.
- Repository description, topics, license, and security policy verified.
- CI completes successfully on the default branch.
- `v0.1.0` tag and GitHub release created.
- Profile README and GitHub Pages link updated to the dedicated repository.
