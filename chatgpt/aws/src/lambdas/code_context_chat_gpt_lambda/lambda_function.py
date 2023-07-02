import json
import requests
import logging
from requests.exceptions import HTTPError, Timeout, RequestException

# Set up logging
logging.basicConfig(level=logging.INFO)

# API URL defined as an environment variable
API_URL = "https://api.bluecollarverse.co.uk/ccp"

# Create a session object to reuse underlying TCP connections
session = requests.Session()


def validate_event(event):
    """
    Validate the incoming event for necessary information
    """
    query_params = event.get("queryStringParameters", {})
    if "query" not in query_params:
        raise ValueError("Query parameter 'query' not provided in the event")
    return query_params["query"]


def make_request(url, params):
    """
    Make a GET request to the given URL with the given parameters.
    """
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        return response.text
    except HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        raise
    except Timeout as err:
        logging.error(f"Timeout occurred: {err}")
        raise
    except RequestException as err:
        logging.error(f"Request failed: {err}")
        raise


def lambda_handler(event, context):
    # Validate incoming event
    try:
        query = validate_event(event)
    except ValueError as err:
        logging.error(f"Invalid event: {err}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(err)}),
        }

    # Make request
    params = {"question": query}
    try:
        response_text = make_request(API_URL, params)
    except HTTPError:
        logging.error("Service unavailable or request rejected")
        return {
            "statusCode": 503,
            "body": json.dumps(
                {
                    "error": "Service unavailable or request rejected",
                }
            ),
        }
    except Timeout:
        logging.error("Request to service timed out")
        return {
            "statusCode": 504,
            "body": json.dumps({"error": "Request to service timed out"}),
        }
    except RequestException as err:
        logging.error(f"Unexpected error: {err}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(err)}),
        }

    # Return successful response
    return {"statusCode": 200, "body": json.dumps({"code": response_text})}
