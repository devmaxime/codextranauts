import toml
import subprocess
import json

# Load the SAM configuration file
config_path = "./aws/samconfig.toml"

try:
    # Load the SAM configuration file
    config = toml.load(config_path)
except Exception:
    print("ERROR: couldn't load toml file.")

# Get the stack name from the configuration file
stack_name = (
    config.get("default", {}).get("deploy", {}).get("parameters", {}).get("stack_name")
)

if not stack_name:
    print("Stack name not found in the configuration file.")

# Call the AWS CLI command with the extracted stack name
try:
    output = subprocess.check_output(
        [
            "aws",
            "cloudformation",
            "describe-stacks",
            "--stack-name",
            stack_name,
            "--query",
            "Stacks[0].Outputs",
            "--output",
            "json",
        ]
    )
    outputs = json.loads(output)
except Exception as e:
    print(f"Error while parsing stack outputs: {e}")


# Now you can use the 'outputs' dictionary in your script
llm_lambda_output = None
codebase_vectorizer_lambda_output = None
for output in outputs:
    if output["OutputKey"] == "LlmLambdaOutput":
        llm_lambda_output = output["OutputValue"]
    elif output["OutputKey"] == "CodebaseVectorizerLambdaOutput":
        codebase_vectorizer_lambda_output = output["OutputValue"]

print(llm_lambda_output, codebase_vectorizer_lambda_output)
