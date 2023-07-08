import os
import json
import tempfile
import pytest
from unittest.mock import patch, mock_open
from aws.api.v1.src.lambdas.team_names_lambda.app import (
    get_team_data, lambda_handler,
    TEAM_DATA_FILE_ERROR, TEAM_DATA_JSON_DECODE_ERROR, UNEXPECTED_ERROR,
    STATUS_CODE_OK, STATUS_CODE_SERVICE_UNAVAILABLE,
    STATUS_CODE_INTERNAL_SERVER_ERROR)

get_team_data_path = "aws.api.v1.src.lambdas.team_names_lambda.app.get_team_data"


# Mocks for JSON data
@pytest.fixture
def team_data():
    return {
        "team_name": "Codextranauts",
        "team_members": [
            {"github": "front-end-guy-2020", "first_name": "Andrey"},
            {"github": "MKCMMSK", "first_name": "Colin"},
            {"github": "Gheeroppa", "first_name": "Federico"},
            {"github": "devmaxime", "first_name": "Maxime"}
        ]
    }


@pytest.fixture
def context_mock():
    return {}


@pytest.fixture
def error_mock():
    return {"error": TEAM_DATA_FILE_ERROR}


@pytest.mark.unit
def test_get_team_data_success(team_data):
    """
    Test successful data retrieval from a temporary JSON file using get_team_data().
    """
    with tempfile.NamedTemporaryFile(suffix=".json", mode='w+t', delete=False) as tmpfile:
        json.dump(team_data, tmpfile)
        tmpfile.flush()

        try:
            assert get_team_data(tmpfile.name) == team_data
        finally:
            os.remove(tmpfile.name)


@pytest.mark.unit
def test_get_team_data_file_not_found():
    """
    Test handling of a FileNotFoundError in get_team_data().
    """
    with patch("builtins.open", side_effect=FileNotFoundError), \
         patch("logging.error") as mock_log:
        assert get_team_data() == {"error": TEAM_DATA_FILE_ERROR}
        mock_log.assert_called_once_with(TEAM_DATA_FILE_ERROR)


@pytest.mark.unit
def test_get_team_data_json_decode_error():
    """
    Ensures get_team_data() handles JSONDecodeError properly and logs an error.
    """
    with patch("builtins.open", mock_open(read_data="not json")) as mock_file, \
         patch("logging.error") as mock_log:
        assert get_team_data() == {"error": TEAM_DATA_JSON_DECODE_ERROR}
        mock_log.assert_called_once_with(TEAM_DATA_JSON_DECODE_ERROR)
        mock_file.assert_called()


@pytest.mark.unit
def test_lambda_handler_success(team_data, context_mock):
    """
    Verifies 'lambda_handler' returns HTTP 200 and correct team data.
    """
    with patch(get_team_data_path, return_value=team_data):
        result = lambda_handler({}, context_mock)
    assert result["statusCode"] == STATUS_CODE_OK, "Expected status code 200"
    assert json.loads(result["body"]) == team_data, "Body content does not match expected team data"


@pytest.mark.unit
def test_lambda_handler_team_data_error(error_mock, context_mock):
    """
    Validates 'lambda_handler' response when team data retrieval fails.
    """
    with patch(get_team_data_path, return_value=error_mock):
        result = lambda_handler({}, context_mock)
    assert result["statusCode"] == STATUS_CODE_SERVICE_UNAVAILABLE, "Expected status code 503"
    assert json.loads(result["body"]) == error_mock, "Error message does not match"


@pytest.mark.unit
def test_lambda_handler_unexpected_error():
    """
    Verifies lambda's handling of an unexpected error.
    """
    with patch(get_team_data_path, side_effect=Exception), \
         patch("logging.error") as mock_log:
        result = lambda_handler({}, context_mock)
        assert result["statusCode"] == STATUS_CODE_INTERNAL_SERVER_ERROR
        assert json.loads(result["body"]) == {"error": UNEXPECTED_ERROR}
        mock_log.assert_called_once()
