import json


def lambda_handler(event, context):
    # Generate a simple Bye World response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Bye, World!"})
    }
    return response
