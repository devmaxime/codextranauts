import json


def lambda_handler(event, context):
    # Generate a simple Hello World response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello, World!"})
    }
    return response
