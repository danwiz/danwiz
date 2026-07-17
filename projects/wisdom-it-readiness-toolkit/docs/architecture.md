# MVP Architecture

## Components

- **Assessment definitions:** versioned JSON or YAML questionnaires and scoring rules
- **Evidence records:** optional references supporting each answer
- **Scoring engine:** deterministic calculation of domain and overall readiness
- **Remediation register:** prioritized findings, owners, due dates, and status
- **Report generator:** Markdown-first summary suitable for HTML or PDF export
- **Interfaces:** Markdown pack first, then CLI, then lightweight web UI

## Readiness domains

1. Strategy and goals
2. Devices and infrastructure
3. Accounts and identity
4. Cybersecurity and resilience
5. Data and information management
6. Software and integrations
7. Digital workplace and collaboration
8. Support, maintenance, and governance

## Maturity scale

- Level 1 — Unprepared
- Level 2 — Basic
- Level 3 — Repeatable
- Level 4 — Managed
- Level 5 — Optimized

## Design principles

- transparent scoring;
- no hidden AI dependency for core assessment results;
- privacy-preserving evidence handling;
- accessible, portable output;
- secure defaults;
- versioned schemas and deterministic tests.

## Release gates

The dedicated repository may be promoted when it has a validated schema, one complete assessment, sample inputs and outputs, automated scoring tests, contribution and security guidance, and a tagged MVP release.
