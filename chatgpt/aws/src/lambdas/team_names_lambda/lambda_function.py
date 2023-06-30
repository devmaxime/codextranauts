import json
import logging
import os
from typing import Dict, Any
from json import JSONDecodeError

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_team_data() -> Dict[str, Any]:
    """Fetches team data from a JSON file.

    This function reads a JSON file named team_data.json located in the
    same directory as this script.
    """
    try:
        json_file = os.path.join(os.path.dirname(__file__), "team.json")
        with open(json_file, "r") as f:
            team_data = json.load(f)
        return team_data
    except FileNotFoundError:
        logging.error("Team data file not found")
        return {"error": "Team data not available"}
    except JSONDecodeError:
        logging.error("Error decoding team data file")
        return {"error": "Team data format is incorrect"}
    except Exception as e:
        logging.error(f"Unexpected error getting team data: {e}")
        raise


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        team_data = get_team_data()

        if "error" in team_data:
            return {
                "statusCode": 503,
                "body": json.dumps({"error": team_data["error"]}),
            }

        logging.info(f"Retrieved team data: {team_data}")

        return {
            "statusCode": 200,
            "body": json.dumps(team_data),
        }
    except Exception as e:
        logging.error(f"Unexpected error in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred"}),
        }
