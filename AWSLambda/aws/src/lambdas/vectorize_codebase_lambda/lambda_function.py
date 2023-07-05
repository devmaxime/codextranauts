import json
import logging
from vectorize_codebase import vectorize_codebase

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        user = body.get("user")
        repo = body.get("repo")

        if user and repo:
            # Call the main function with the extracted URL
            vectorize_codebase(user, repo)
            return create_response(
                200,
                "Lambda function executed successfully!"
            )
        else:
            return create_response(
                400, "Missing or invalid 'url' parameter in the request body."
            )
    except json.JSONDecodeError as e:
        logger.error("JSONDecodeError: %s", e)
        return create_response(
            400,
            "Invalid input format. Expecting a JSON body.",
        )
    except Exception as e:
        logger.error("An error occurred: %s", e)
        return create_response(
            500,
            "An error occurred while processing the request.",
        )
