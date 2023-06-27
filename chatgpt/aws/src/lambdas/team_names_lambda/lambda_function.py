import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "team_name": "Codextranauts",
            "team_members": [
                {
                    "github": "front-end-guy-2020",
                    "first_name": "Andrey",
                },
                {
                    "github": "MKCMMSK",
                    "first_name": "Colin"
                },
                {
                    "github": "Gheeroppa",
                    "first_name": "Federico"
                },
                {
                    "github": "devmaxime",
                    "first_name": "Maxime"
                },
            ]
        })
    }
