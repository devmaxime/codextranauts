import json
import requests


def lambda_handler(event, context):
    # Get the 'query' from the body
    query = event["query"]

    if query is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No query provided"}),
        }

    # Define the URL and query parameters for the API request
    url = "https://codextranauts-c8f0a4d4554f.herokuapp.com/qa"
    params = {"question": query}

    try:
        # Make the POST request
        response = requests.post(url, params=params)
        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        return {"statusCode": 500, "body": json.dumps({"error": str(err)})}

    else:
        # Return the response body as the result of the Lambda function
        return {"statusCode": 200, "body": {"code": response.text}}
