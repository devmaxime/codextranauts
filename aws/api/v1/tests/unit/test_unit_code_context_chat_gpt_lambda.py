import pytest
from http import HTTPStatus
from aws.api.v1.src.lambdas.code_context_chat_gpt_lambda.app import (
    validate_event,
    make_llm_request,
    lambda_handler,
    lambda_client,
)


@pytest.mark.unit
def test_validate_event_missing_query():
    with pytest.raises(ValueError):
        validate_event({"queryStringParameters": {}})


@pytest.mark.unit
def test_validate_event_empty_query():
    with pytest.raises(ValueError):
        validate_event({"queryStringParameters": {"query": ""}})


@pytest.mark.unit
def test_validate_event_valid_query():
    result = validate_event({"queryStringParameters": {"query": "myquery"}})
    assert result == "myquery"


@pytest.mark.unit
def test_make_llm_request(mocker):
    mock_payload = {"Payload": mocker.Mock(read=lambda: b'{"response": "ok"}')}

    mocker.patch.object(lambda_client, "invoke", return_value=mock_payload)

    result = make_llm_request({"question": "myquery"})
    assert result == {"response": "ok"}


@pytest.mark.unit
def test_lambda_handler(mocker):
    mocker.patch(
        "aws.api.v1.src.lambdas.code_context_chat_gpt_lambda.app.validate_event",
        return_value="myquery",
    )
    mocker.patch(
        "aws.api.v1.src.lambdas.code_context_chat_gpt_lambda.app.make_llm_request",
        return_value="ok",
    )
    result = lambda_handler({"queryStringParameters": {"query": "myquery"}}, {})
    assert result == {"statusCode": HTTPStatus.OK, "body": '{"code": "ok"}'}
