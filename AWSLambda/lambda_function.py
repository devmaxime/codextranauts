from main import main
import json


def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])

        # Extract the 'url' variable
        url = body['url']

        main(url)

        return {"statusCode": 200, "body": "Lambda function executed successfully!"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
