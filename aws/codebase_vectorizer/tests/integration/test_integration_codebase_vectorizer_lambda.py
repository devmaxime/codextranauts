import json
import pytest
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

# ARN of the Lambda function you want to test
CODEBASE_VECTORIZER_LAMBDA_ARN = os.getenv("CODEBASE_VECTORIZER_LAMBDA_ARN")


@pytest.mark.integration
def test_lambda_handler_integration():
    """Test if the deployed lambda function correctly returns the expected result."""
    if not CODEBASE_VECTORIZER_LAMBDA_ARN:
        pytest.skip(
            "Skipping test because CODEBASE_VECTORIZER_LAMBDA_ARN environment variable is not set"
        )
    client = boto3.client("lambda")

    # Define the input for the Lambda function
    payload = {"queryStringParameters": {"query": "myquery"}}

    # The payload that the Lambda function will receive is a JSON-formatted string
    payload_str = json.dumps(payload)

    # The payload has to be bytes
    payload_bytes_arr = bytes(payload_str, encoding="utf8")

    try:
        # Invoke the Lambda function
        response = client.invoke(
            FunctionName=CODEBASE_VECTORIZER_LAMBDA_ARN,
            InvocationType="RequestResponse",
            Payload=payload_bytes_arr,
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Error invoking Lambda function: {error}")
        assert False

    # Parse response
    response_payload = response["Payload"].read().decode("utf-8")
    response_payload_dict = json.loads(response_payload)

    # Make sure the response is what we expect
    assert response_payload_dict == "vectorizer"
