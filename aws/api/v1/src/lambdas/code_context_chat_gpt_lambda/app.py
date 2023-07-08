import json
import requests
import logging
from requests.exceptions import HTTPError, Timeout, RequestException

# Set up logging
logging.basicConfig(level=logging.INFO)

# API URL defined as an environment variable
API_URL = "todo_lambda_endpoint"

# Create a session object to reuse underlying TCP connections
session = requests.Session()


def validate_event(event):
    """
    Validate the incoming event for necessary information
    """
    query_params = event.get("queryStringParameters", {})
    if "query" not in query_params:
        raise ValueError(
            "Query parameter 'query' not provided in the event"
        )

    query = query_params.get("query")

    # Check if query is an empty string
    if query.strip() == "":
        raise ValueError(
            "Query parameter 'query' should not be an empty string"
        )

    return query


def make_llm_request(url, params):
    """
    Make a GET request to the given URL with the given parameters.
    """
    return "llm response"


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
        response_text = make_llm_request(API_URL, params)
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
