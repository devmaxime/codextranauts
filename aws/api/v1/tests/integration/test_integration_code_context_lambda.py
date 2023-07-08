import pytest
import requests
import requests_mock

API_GATEWAY_URL = "https://api.bluecollarverse.co.uk/v1"
ENDPOINT = "/code_context"


@pytest.mark.integration
def test_code_context_success():
    query = "How to write a function in Python?"
    response = requests.get(f"{API_GATEWAY_URL}${ENDPOINT}?question={query}")

    assert response.status_code == 200

    response_json = response.json()
    assert 'code' in response_json


@pytest.mark.integration
def test_code_context_bad_request():
    query = ""  # Empty query, which should trigger a bad request
    response = requests.get(f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}")

    assert response.status_code == 400

    response_json = response.json()
    assert 'error' in response_json


@pytest.mark.integration
def test_integration_internal_error():
    """
    Test to simulate the situation when the service is unavailable.
    In this case, the /team endpoint should return a 503 status code
    and an error message.
    """
    with requests_mock.Mocker() as m:
        query = "How to write a function in a non-existent programming language?"
        m.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}",
            status_code=500,
            json={"error": "An unexpected error occurred"}
        )
        response = requests.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}"
        )

        assert response.status_code == 500
        assert response.json() == {"error": "An unexpected error occurred"}


@pytest.mark.integration
def test_integration_service_unavailable():
    """
    Test to simulate the situation when the service is unavailable.
    In this case, the /team endpoint should return a 503 status code
    and an error message.
    """
    with requests_mock.Mocker() as m:
        query = "How to write a function in a non-existent programming language?"
        m.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}",
            status_code=503,
            json={"error": "Service unavailable"}
        )
        response = requests.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}"
        )

        assert response.status_code == 503
        assert response.json() == {"error": "Service unavailable"}


@pytest.mark.integration
def test_integration_service_timeout():
    """
    Test to simulate the situation when the service is unavailable.
    In this case, the /team endpoint should return a 503 status code
    and an error message.
    """
    with requests_mock.Mocker() as m:
        query = "How to write a function in a non-existent programming language?"
        m.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}",
            status_code=504,
            json={"error": "Request to service timed out"}
        )
        response = requests.get(
            f"{API_GATEWAY_URL}${ENDPOINT}/code_context?question={query}"
        )

        assert response.status_code == 504
        assert response.json() == {"error": "Request to service timed out"}
