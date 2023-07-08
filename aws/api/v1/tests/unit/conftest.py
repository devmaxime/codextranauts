import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def app_module():
    import aws.api.v1.src.lambdas.code_context_chat_gpt_lambda.app as app_module

    return app_module
