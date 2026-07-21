# GitHub Actions and AI-Credit Cost Controls

## Purpose

Keep GitHub automation and AI-assisted development within predictable free-tier or approved spending limits.

## Current operating position

- Prefer public repositories for portfolio and open-source work so standard GitHub-hosted Actions remain free.
- Treat private-repository Actions minutes, artifact storage, cache storage, Codespaces usage, and Copilot AI credits as metered resources.
- Do not enable paid overages without explicit approval.

## Required controls

1. Configure account-level budgets and alerts for GitHub Actions and Copilot AI credits.
2. Enable alerts at 75%, 90%, and 100% where supported.
3. Use the stop-usage option for metered products when the budget limit is reached.
4. Keep default workflow permissions read-only and grant write scopes only to jobs that require them.
5. Avoid unnecessary matrix builds, duplicate operating-system runs, and scheduled workflows with no material output.
6. Use concurrency cancellation for superseded branch and pull-request runs.
7. Set short artifact-retention periods for temporary validation evidence.
8. Cache dependencies only when the cache materially reduces runtime and storage remains controlled.
9. Review Actions usage and Copilot AI-credit consumption monthly.
10. Record any approved paid usage with purpose, owner, repository, expected benefit, and expiration date.

## Repository workflow standard

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
```

Artifact uploads should specify an intentional retention period:

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: validation-evidence
    path: build/evidence/
    retention-days: 14
```

## Decision rules

- **Public portfolio and open-source CI:** use standard hosted runners unless a security or platform requirement justifies another runner.
- **Private repositories:** estimate monthly minutes before adding matrix jobs, scheduled scans, or repeated documentation builds.
- **Copilot and AI agents:** use included AI credits first; establish a hard budget before enabling additional metered usage.
- **Release evidence:** retain long-lived evidence in releases or repository documentation; do not use expensive workflow-artifact retention as permanent storage.

## Review cadence

Review usage monthly and after any major workflow, repository-visibility, Copilot-plan, or billing-model change.
