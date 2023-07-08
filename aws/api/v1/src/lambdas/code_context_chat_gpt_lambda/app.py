import os
import json
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from http import HTTPStatus
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get env vars
LLM_LAMBDA_ARN = os.getenv("LLM_LAMBDA_ARN")

if not LLM_LAMBDA_ARN:
    raise ValueError("Missing environment variable: LLM_LAMBDA_ARN")


lambda_client = boto3.client("lambda")


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            return {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": json.dumps({"error": str(err)}),
            }
        except (BotoCoreError, ClientError) as err:
            logger.error(f"Error calling Lambda function: {str(err)}")
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"error": str(err)}),
            }

    return wrapper


def validate_event(event):
    """
    Validate the incoming event for necessary information
    """
    query_params = event.get("queryStringParameters", {})
    if "query" not in query_params:
        logger.error('Missing "query" in queryStringParameters.')
        raise ValueError("Query parameter 'query' not provided in the event")

    query = query_params.get("query")
    if not query.strip():
        logger.error('"query" parameter is empty.')
        raise ValueError("Query parameter 'query' should not be an empty string")

    return query


def make_llm_request(params):
    try:
        invoke_response = lambda_client.invoke(
            FunctionName=LLM_LAMBDA_ARN,
            InvocationType="RequestResponse",
            Payload=json.dumps(params),
        )
    except (BotoCoreError, ClientError) as error:
        logger.error(f"Error calling Lambda function: {str(error)}")
        raise error

    payload = json.loads(invoke_response["Payload"].read().decode("utf-8"))
    return payload


@error_handler
def lambda_handler(event, context):
    query = validate_event(event)
    params = {"question": query}
    response_text = make_llm_request(params)
    return {"statusCode": HTTPStatus.OK, "body": json.dumps({"code": response_text})}
