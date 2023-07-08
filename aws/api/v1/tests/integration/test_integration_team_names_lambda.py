import requests
import requests_mock
import pytest

API_GATEWAY_URL = "https://api.bluecollarverse.co.uk/v1"


@pytest.fixture
def api_response():
    """Fixture to make a GET request to the /team endpoint and yield the
    response."""
    response = requests.get(API_GATEWAY_URL + "/team")
    yield response


@pytest.mark.integration
def test_integration_success(api_response):
    """
    Test to ensure that the /team endpoint returns a 200 status code,
    and the response contains valid team information.
    """
    response_data = api_response.json()

    assert api_response.status_code == 200
    assert response_data, "Response JSON is empty"

    assert "team_name" in response_data, "team_name is not in the response"
    assert response_data["team_name"], "team_name is empty"

    assert "team_members" in response_data, "team_members is not in the response"
    assert response_data["team_members"], "team_members is empty"
    assert isinstance(response_data["team_members"], list), "team_members is not a list"

    assert (
        len(response_data["team_members"]) >= 1
    ), "No team members found in the response"

    for member in response_data["team_members"]:
        assert "github" in member, "github is not in the team member's data"
        assert "first_name" in member, "first_name is not in the team member's data"


@pytest.mark.integration
def test_integration_internal_error():
    """
    Test to simulate the situation when the server encounters an unexpected
    error. In this case, the /team endpoint should return a 500 status code
    and an error message.
    """
    with requests_mock.Mocker() as m:
        m.get(
            API_GATEWAY_URL + "/team",
            status_code=500,
            json={"error": "An unexpected error occurred"},
        )
        response = requests.get(API_GATEWAY_URL + "/team")
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
        m.get(
            API_GATEWAY_URL + "/team",
            status_code=503,
            json={"error": "Service unavailable"},
        )
        response = requests.get(API_GATEWAY_URL + "/team")

        assert response.status_code == 503
        assert response.json() == {"error": "Service unavailable"}
