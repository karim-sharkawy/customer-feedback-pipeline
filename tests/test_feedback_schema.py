# Tests for the canonical custoemr feedback schema

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from api.schemas import FeedbackRecord


@pytest.fixture
def valid_feedback() -> dict:
    # Return a valid example feedback record

    return {
        "feedback_id": "review-001",
        "product_id": "B000000001",
        "text": "The product works well.",
        "created_at": "2025-03-14T12:30:00Z",
        "title": "Good quality",
        "rating": 5,
        "product_variant": None,
        "helpful_votes": 3,
    }

def test_valid_feedback_is_accepted(valid_feedback: dict) -> None:
    record = FeedbackRecord.model_validate(valid_feedback)

    assert record.feedback_id == "review-001"
    assert record.product_id == "B000000001"
    assert record.text == "The product works well."
    assert record.rating == 5
    assert record.helpful_votes == 3

def test_timestamp_is_normalized_to_utc(valid_feedback: dict) -> None:
    valid_feedback["created_at"] = "2025-03-14T08:30:00-04:00"

    record = FeedbackRecord.model_validate(valid_feedback)

    assert record.created_at == datetime(
        2025, 3, 14, 12, 30, tzinfo=timezone.utc
    )
    assert record.created_at.utcoffset().total_seconds() == 0


def test_timezone_naive_timestamp_is_assumed_utc(valid_feedback: dict) -> None:
    valid_feedback["created_at"] = "2025-03-14T12:30:00"

    record = FeedbackRecord.model_validate(valid_feedback)

    assert record.created_at == datetime(
        2025, 3, 14, 12, 30, tzinfo=timezone.utc
    )


@pytest.mark.parametrize(
    "field",
    ["feedback_id", "product_id", "text"],
)
def test_required_string_fields_reject_blank_values(valid_feedback: dict, field: str) -> None:
    valid_feedback[field] = "   "

    with pytest.raises(ValidationError):
        FeedbackRecord.model_validate(valid_feedback)


@pytest.mark.parametrize("rating", [0, 6, -1])
def test_rating_must_be_between_one_and_five(valid_feedback: dict, rating: int) -> None:
    valid_feedback["rating"] = rating

    with pytest.raises(ValidationError):
        FeedbackRecord.model_validate(valid_feedback)


@pytest.mark.parametrize("helpful_votes", [-1, -10])
def test_helpful_votes_cannot_be_negative(valid_feedback: dict, helpful_votes: int) -> None:
    valid_feedback["helpful_votes"] = helpful_votes

    with pytest.raises(ValidationError):
        FeedbackRecord.model_validate(valid_feedback)


def test_optional_fields_can_be_null(valid_feedback: dict) -> None:
    valid_feedback["title"] = None
    valid_feedback["rating"] = None
    valid_feedback["product_variant"] = None
    valid_feedback["helpful_votes"] = None

    record = FeedbackRecord.model_validate(valid_feedback)

    assert record.title is None
    assert record.rating is None
    assert record.product_variant is None
    assert record.helpful_votes is None


def test_blank_optional_strings_become_none(valid_feedback: dict) -> None:
    valid_feedback["title"] = "   "
    valid_feedback["product_variant"] = ""

    record = FeedbackRecord.model_validate(valid_feedback)

    assert record.title is None
    assert record.product_variant is None


def test_unexpected_fields_are_rejected(valid_feedback: dict) -> None:
    valid_feedback["unexpected_field"] = "not part of the schema"

    with pytest.raises(ValidationError):
        FeedbackRecord.model_validate(valid_feedback)


def test_invalid_timestamp_is_rejected(valid_feedback: dict) -> None:
    valid_feedback["created_at"] = "not-a-timestamp"

    with pytest.raises(ValidationError):
        FeedbackRecord.model_validate(valid_feedback)


def test_model_can_be_serialized_to_json(valid_feedback: dict) -> None:
    record = FeedbackRecord.model_validate(valid_feedback)

    serialized = record.model_dump(mode="json")

    assert serialized["feedback_id"] == "review-001"
    assert serialized["created_at"] == "2025-03-14T12:30:00Z"
