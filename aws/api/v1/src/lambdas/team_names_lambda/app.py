import json
import logging
import os
from typing import Dict, Any
from json import JSONDecodeError

# Set up logging
logging.basicConfig(level=logging.INFO)


# Constants
STATUS_CODE_OK = 200
STATUS_CODE_SERVICE_UNAVAILABLE = 503
STATUS_CODE_INTERNAL_SERVER_ERROR = 500

TEAM_DATA_FILE_ERROR = "Team data file not found"
TEAM_DATA_JSON_DECODE_ERROR = "Team data format is incorrect"
UNEXPECTED_ERROR = "An unexpected error occurred"


def get_team_data(json_file=None) -> Dict[str, Any]:
    """Fetches team data from a JSON file.
    Reads a JSON file located in the same directory as this
    script by default, or at a different location if specified.
    """
    try:
        if json_file is None:
            json_file = os.path.join(os.path.dirname(__file__), "team.json")
        with open(json_file, "r") as f:
            team_data = json.load(f)
        return team_data
    except FileNotFoundError:
        logging.error(TEAM_DATA_FILE_ERROR)
        return {"error": TEAM_DATA_FILE_ERROR}
    except JSONDecodeError:
        logging.error(TEAM_DATA_JSON_DECODE_ERROR)
        return {"error": TEAM_DATA_JSON_DECODE_ERROR}
    except Exception as e:
        logging.error(f"Unexpected error getting team data: {e}")
        raise


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        team_data = get_team_data()

        if "error" in team_data:
            return {
                "statusCode": STATUS_CODE_SERVICE_UNAVAILABLE,
                "body": json.dumps({"error": team_data["error"]}),
            }

        logging.info(f"Retrieved team data: {team_data}")

        return {
            "statusCode": STATUS_CODE_OK,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "https://docs.bluecollarverse.co.uk",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(team_data),
        }
    except Exception as e:
        logging.error(f"Unexpected error in lambda_handler: {e}")
        return {
            "statusCode": STATUS_CODE_INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": UNEXPECTED_ERROR}),
        }
