import logging
from importlib import import_module
from dotenv import load_dotenv
from shared_code.config import settings
from shared_code.llm.openai import get_gpt_3_5_turbo_llm
from shared_code.agents.custom_agent import get_custom_agent
from shared_code.tools.deeplake_codebase_tool import get_deeplake_codebase_tool
from shared_code.tools.pinecone_codebase_tool import get_pinecone_codebase_tool


load_dotenv()


log = logging.getLogger("uvicorn")


def get_agent_dependency():
    log.info(f"Initializing LLM {settings.llm_model_name}...")
    try:
        if settings.llm_model_name == "gpt-3.5-turbo":
            llm = get_gpt_3_5_turbo_llm()
        else:
            log.error(f"Unknown LLM model name: {settings.llm_model_name}")
            raise ValueError(f"Unknown LLM model name: {settings.llm_model_name}")
    except Exception as e:
        log.error(f"Could not initialize LLM {settings.llm_model_name}: {e}")
        raise e

    log.info("Initializing agent...")
    try:
        # Get the template
        template_module = import_module(
            f"shared_code.templates.{settings.template_name}"
        )
        template = template_module.template

        # Get the tools
        if settings.vector_db == "deeplake":
            tools = [get_deeplake_codebase_tool()]
        elif settings.vector_db == "pinecone":
            tools = [get_pinecone_codebase_tool()]
        else:
            log.error(f"Unknown vector database: {settings.vector_db}")

        # Get the agent
        agent = get_custom_agent(llm, template, tools)
    except Exception as e:
        log.error(f"Could not initialize agent: {e}")
        raise e

    return agent


def lambda_handler(event, context):
    # Getting question from body
    question = event['queryStringParameters']['question']

    # here we need to run LLM
    agent = get_agent_dependency()
    llm_result = agent.run(question)

    return {
        "statusCode": 200,
        "body": llm_result,
    }
