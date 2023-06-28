import json
import logging
from urllib.parse import urlparse
from main import process_codebase

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


def create_response(status_code: int, message: str):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }


def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get("body", {}))

        # Extract the 'url' variable
        url = body.get("url")

        if url and is_valid_url(url):
            # Call the main function with the extracted URL
            process_codebase(url)
            return create_response(200, "Lambda function executed successfully!")
        else:
            return create_response(
                400, "Missing or invalid 'url' parameter in the request body."
            )
    except json.JSONDecodeError as e:
        logger.error("JSONDecodeError: %s", e)
        return create_response(400, "Invalid input format. Expecting a JSON body.")
    except Exception as e:
        logger.error("An error occurred: %s", e)
        return create_response(500, "An error occurred while processing the request.")
