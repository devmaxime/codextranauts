import requests


class TestEndpointIntegration:
    def setup_class(self):
        self.base_url = 'https://api.bluecollarverse.co.uk/v1'

    def test_hello_world_endpoint(self):
        response = requests.get(f'{self.base_url}/hello')

        # Check the HTTP status code
        assert response.status_code == 200

        # Check the response body
        assert response.json() == {"message": "Hello, World!"}
