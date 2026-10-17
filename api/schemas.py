### Canonical data schemas for custoemr feedback records

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FeedbackRecord(BaseModel):
    # A normalized customer feedback record used by the NLP pipeline

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "feedback_id": "example-review-001",
                    "product_id": "B000000001",
                    "text": "The product works well and feels durable.",
                    "created_at": "2025-03-14T12:30:00Z",
                    "title": "Good quality",
                    "rating": 5,
                    "product_variant": None,
                    "helpful_votes": 3,
                }
            ]
        },
    )

    feedback_id: str = Field(
        min_length=1,
        description="Stable identifier for the source feedback record.",
    )

    product_id: str = Field(
        min_length=1,
        description="Identifier of the product associated with the feedback.",
    )

    text: str = Field(
        min_length=1,
        description="Main feedback text used by NLP components.",
    )

    created_at: datetime = Field(
        description="Timestamp of the feedback, normalized to UTC.",
    )

    title: str | None = Field(
        default=None,
        description="Optional title associated with the feedback.",
    )

    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Optional star rating on a scale from 1 to 5.",
    )

    product_variant: str | None = Field(
        default=None,
        description="Optional product variation, such as size or color.",
    )

    helpful_votes: int | None = Field(
        default=None,
        ge=0,
        description="Optional nonnegative count of helpful votes.",
    )

    @field_validator("feedback_id", "product_id")
    @classmethod
    def identifiers_must_not_be_blank(cls, value: str) -> str:
        """Reject identifiers that contain only whitespace."""
        if not value:
            raise ValueError("Identifier must not be blank.")
        return value

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        # Reject empty or whitespace-only feedback text
        if not value:
            raise ValueError("Feedback text must not be blank.")
        return value

    @field_validator("title", "product_variant")
    @classmethod
    def empty_optional_strings_become_none(
        cls, value: str | None
    ) -> str | None:
        # Represent blank optional strings consistently as None
        if value == "":
            return None
        return value

    @field_validator("created_at")
    @classmethod
    def normalize_timestamp_to_utc(cls, value: datetime) -> datetime:
        """Normalize timestamps to UTC.

        Assumption: timestamps without timezone information are UTC.
        Confirm this assumption against the source dataset before relying
        on timestamps for chronological analysis.
        """
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
