import pytest
from aws.codebase_vectorizer.src.lambdas.codebase_vectorizer_lambda.app import (
    lambda_handler,
)


@pytest.mark.unit
def test_lambda_handler_with_valid_event():
    """Test if lambda_handler returns the correct response when called with a valid event."""
    event = {"queryStringParameters": {"query": "myquery"}}
    context = {}

    result = lambda_handler(event, context)

    assert result == "vectorizer"


@pytest.mark.unit
def test_lambda_handler_with_empty_event():
    """Test if lambda_handler returns the correct response when called with an empty event."""
    event = {}
    context = {}

    result = lambda_handler(event, context)

    assert result == "vectorizer"


@pytest.mark.unit
def test_lambda_handler_with_none_event():
    """Test if lambda_handler returns the correct response when called with a None event."""
    event = None
    context = {}

    result = lambda_handler(event, context)

    assert result == "vectorizer"
