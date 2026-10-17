
# Feedback Data Schema

## 1. Purpose

This document defines the canonical feedback record used by the
Customer Feedback Pipeline.

The schema provides a consistent data contract for ingestion,
preprocessing, NLP model training, inference, and future storage
in PostgreSQL or other systems.

The project uses Pydantic to enforce this contract in Python.
Database schemas and distributed-processing schemas may implement
the same contract when those components are introduced.

## 2. Design principles

- Preserve the original dataset in the raw-data layer.
- Normalize source-specific field names into a canonical schema.
- Separate raw source data from validated NLP-ready records.
- Make required and optional fields explicit.
- Validate data types and domain constraints.
- Keep source identifiers for traceability and deduplication.
- Avoid storing fields that are unnecessary for the initial NLP task.
- Keep source metadata available when it supports evaluation,
  analysis, or future extensions.

## 3. Canonical record

A canonical feedback record contains the following fields.

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `feedback_id` | String | Yes | Must not be blank | Stable identifier for the source feedback record. |
| `product_id` | String | Yes | Must not be blank | Identifier of the associated product. |
| `text` | String | Yes | Must not be blank | Main feedback text used by NLP components. |
| `created_at` | Datetime | Yes | Normalized to UTC | Timestamp associated with the feedback. |
| `title` | String or null | No | Blank values normalize to null | Optional review title. |
| `rating` | Integer or null | No | 1 through 5 when present | Optional star rating. |
| `product_variant` | String or null | No | Blank values normalize to null | Optional product variation information. |
| `helpful_votes` | Integer or null | No | Must be nonnegative when present | Number of helpful votes associated with the review. |

### Required versus optional

Required fields must be present and valid for a record to qualify
as a canonical feedback record.

The `text` field is required because this schema represents
NLP-ready feedback. Records without usable text remain part of the
raw source data but cannot pass this contract.

The other required fields support traceability, product-level
analysis, and temporal analysis.

Optional fields are permitted to be absent or null. Their absence
must not prevent a record from being processed when the required
fields are valid.

A source dataset may have stricter requirements than this general
contract. For example, Amazon reviews normally provide a rating,
even though other feedback sources may not.

## 4. Source dataset

Initial source:

`datahiveai/Amazon-Reviews-Dataset`

The source dataset contains approximately 255,966 review records
in the version inspected during development.

The source columns are mapped to the canonical schema as follows.

| Amazon source field | Canonical field | Action |
|---|---|---|
| `id` | `feedback_id` | Rename and preserve as a string. |
| `asin` | `product_id` | Rename and preserve as a string. |
| `body` | `text` | Rename and validate as nonblank text. |
| `date` | `created_at` | Parse as a datetime and normalize to UTC. |
| `title` | `title` | Preserve when available. |
| `stars` | `rating` | Rename and validate as an integer from 1 to 5. |
| `variation` | `product_variant` | Rename; missing values become null. |
| `found_helpful` | `helpful_votes` | Rename and validate as a nonnegative integer. |
| `verified_purchase` | None | Excluded from the initial canonical schema. |
| `url` | None | Excluded; not needed for the initial NLP workflow. |
| `images` | None | Excluded; image processing is outside the project scope. |
| `videos` | None | Excluded; video processing is outside the project scope. |
| `user_id` | None | Excluded from the initial schema; reviewer-level analysis is not currently required. |

The original source file should retain its original fields.
The mapping above applies to canonical records, not to the raw
source file.

## 5. Missing values and validation

The inspected dataset contains missing values in several fields,
including `body`, `title`, `variation`, `user_id`, and
`verified_purchase`.

The canonical schema applies these rules:

- Missing or blank `text` is invalid for an NLP-ready record.
- Missing `feedback_id`, `product_id`, or `created_at` is invalid.
- Missing `title`, `rating`, `product_variant`, or `helpful_votes`
  is permitted.
- A rating outside the range 1 through 5 is invalid.
- Negative helpful-vote counts are invalid.
- Timestamps are normalized to UTC.
- A timestamp without timezone information is currently assumed
  to be UTC. This assumption must be confirmed against the source.
- Unexpected fields are rejected by the canonical Pydantic model.

Invalid records should be reported and retained in the raw-data
layer for inspection. They should not be silently discarded.

Detailed ingestion-time validation, error reporting, and handling
of invalid records will be implemented separately.

## 6. Example record

The following is an illustrative canonical record, not an actual
record extracted from the dataset.

```json
{
  "feedback_id": "example-review-001",
  "product_id": "B000000001",
  "text": "The product works well and feels durable.",
  "created_at": "2025-03-14T12:30:00Z",
  "title": "Good quality",
  "rating": 5,
  "product_variant": null,
  "helpful_votes": 3
}
```

## 7. Relationship to NLP tasks

The `text` field is the primary input to the initial NLP pipeline.
The `title` field may later be combined with the review body if
experiments show that doing so improves performance.

The `rating` field can provide a weakly supervised sentiment label.
However, a star rating is not necessarily equivalent to the
sentiment expressed in the review text.

Derived sentiment labels and model predictions should be tracked
separately from the original source rating.

The product identifier and timestamp support grouped evaluation,
chronological evaluation, and analysis of changes in feedback
over time. These fields are metadata, not automatically NLP
model inputs.

## 8. Future implementation

This contract will be reused as the project develops:

- Python and Pydantic for application-level validation.
- FastAPI for future request and response validation.
- PostgreSQL for persistent storage, with matching database
  types and constraints.
- PySpark for distributed processing when required by dataset
  size or workload.
- MLflow and model-training pipelines for experiment tracking
  and reproducible evaluation.

Each implementation should preserve the meaning of the canonical
fields and their constraints.
