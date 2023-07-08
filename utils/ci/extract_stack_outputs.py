import toml
import subprocess
import json

# Load the SAM configuration file
config = toml.load("aws/samconfig.toml")

# Get the stack name from the configuration file
stack_name = config["default"]["deploy"]["parameters"]["stack_name"]

# Call the AWS CLI command with the extracted stack name
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

# Now you can use the 'outputs' dictionary in your script
llm_lambda_output = None
codebase_vectorizer_lambda_output = None
for output in outputs:
    if output["OutputKey"] == "LlmLambdaOutput":
        llm_lambda_output = output["OutputValue"]
    elif output["OutputKey"] == "CodebaseVectorizerLambdaOutput":
        codebase_vectorizer_lambda_output = output["OutputValue"]

print(llm_lambda_output, codebase_vectorizer_lambda_output)
