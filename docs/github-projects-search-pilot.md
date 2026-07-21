# GitHub Projects Advanced Search Pilot

## Pilot scope

Use the Wisdom IT Readiness Toolkit `v0.2.0` roadmap as the first controlled test of advanced GitHub Projects search.

Parent issue:

- `danwiz/wisdom-it-readiness-toolkit#5`

Child work packages:

- `#6` Requirements, compatibility, and acceptance baseline
- `#7` Prioritized recommendations
- `#8` Packaging, installed CLI behavior, and errors
- `#9` Richer reporting, release validation, and portfolio integration

## Recommended project fields

| Field | Type | Example values |
|---|---|---|
| Status | Single select | Backlog, Ready, In progress, Review, Validation, Done |
| Phase | Single select | Requirements, Design, Implementation, Verification, Release |
| Priority | Single select | Critical, High, Medium, Low |
| Workstream | Single select | Assessment, Recommendations, Packaging, Reporting, Portfolio |
| Release | Text or iteration | v0.2.0 |
| Risk | Single select | High, Medium, Low |
| Target date | Date | Planned completion date |
| Parent | Text | #5 |

## Saved-view search tests

Create and validate views equivalent to the following logic:

```text
Release:"v0.2.0" AND Status:"In progress"
```

```text
Release:"v0.2.0" AND (Phase:"Verification" OR Status:"Validation")
```

```text
Release:"v0.2.0" AND Risk:"High" AND -Status:"Done"
```

```text
Parent:"#5" AND (Priority:"Critical" OR Priority:"High")
```

```text
Release:"v0.2.0" AND -Status:"Done" AND target-date:<@today
```

## Views

1. **Release control table** — all parent and child items with phase, status, risk, and target date.
2. **Delivery board** — grouped by status.
3. **Waterfall stage-gate view** — grouped by phase.
4. **Validation queue** — verification, security, documentation, and release-gate items.
5. **Executive risk view** — open high-risk and overdue items.

## Success criteria

- Parent and child work are visible in one project.
- Search expressions return expected issue sets.
- Waterfall phases and iterative delivery status can coexist without duplicate tracking.
- Overdue, high-risk, blocked, and validation-ready work can be isolated quickly.
- The model is reusable for Sports Management System publication and later consulting projects.

## Constraint

This document defines the pilot. Creating or changing the live GitHub Project views remains a deliberate account-level action and should be validated in the GitHub interface.
