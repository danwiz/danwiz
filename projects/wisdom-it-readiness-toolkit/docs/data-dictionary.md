# Data Dictionary

## Assessment document

| Field | Type | Required | Description |
|---|---|---:|---|
| `assessment_id` | string | yes | Stable governed identifier for the assessment. |
| `title` | string | yes | Human-readable assessment title. |
| `version` | string | yes | Semantic version of the assessment definition. |
| `status` | string | yes | Lifecycle state such as `governed-working-draft`. |
| `scale` | object | yes | Allowed response values and labels. |
| `domains` | array | yes | Readiness domains included in scoring. |
| `maturity_bands` | array | yes | Percentage ranges mapped to maturity levels. |

## Domain object

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | yes | Stable machine-readable domain key. |
| `title` | string | yes | Human-readable domain name. |
| `questions` | array | yes | Questions assigned to the domain. |

## Question object

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | yes | Stable question identifier. |
| `prompt` | string | yes | Assessment statement or question. |
| `weight` | number | yes | Positive contribution to weighted scoring. |

## Response document

The response document is a JSON object whose keys are question identifiers and whose values are integers allowed by the assessment scale.

```json
{
  "STR-01": 2,
  "STR-02": 1,
  "INF-01": 2
}
```

## Scoring output

| Field | Type | Description |
|---|---|---|
| `overall_percent` | number | Weighted readiness percentage from 0 to 100. |
| `maturity_level` | integer | Maturity level from 1 to 5. |
| `maturity_label` | string | Human-readable maturity label. |
| `domain_scores` | object | Percentage result for each answered domain. |
| `unanswered_questions` | array | Question IDs without responses. |

## Data-quality rules

- Unknown question IDs are rejected.
- Response values outside the declared scale are rejected.
- Weights must be positive numbers.
- At least one valid response is required.
- Missing responses are reported and excluded rather than silently assigned a value.
