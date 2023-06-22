from fastapi import APIRouter, Depends
import logging

from config import settings
from llm.openai import get_gpt_3_5_turbo_llm
from agents.custom_agent import get_agent
from templates import template_1
from tools.deeplake_codebase_tool import get_deeplake_codebase_tool

router = APIRouter()
log = logging.getLogger("uvicorn")

def get_agent_dependency():
    log.info(f"Initializing LLM {settings.llm_model_name}...")
    try:
        match settings.llm_model_name:
            case "gpt-3.5-turbo":
                llm = get_gpt_3_5_turbo_llm()
            case _:
                log.error(f"Unknown LLM model name: {settings.llm_model_name}")
                raise ValueError(f"Unknown LLM model name: {settings.llm_model_name}")
    except Exception as e:
        log.error(f"Could not initialize LLM {settings.llm_model_name}: {e}")
        raise e

    log.info("Initializing agent...")
    try:
        template = template_1.template
        tools = [get_deeplake_codebase_tool()]
        agent = get_agent(llm, template, tools)
    except Exception as e:
        log.error(f"Could not initialize agent: {e}")
        raise e

    return agent

@router.post("/qa/")
async def qa_endpoint(question: str, agent=Depends(get_agent_dependency)):
    return agent.run(question)
