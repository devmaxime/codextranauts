from langchain.chat_models import ChatOpenAI


def get_gpt_3_5_turbo_llm():
    """
    Create a custom LLM based on the gpt-3.5-turbo model.

    Returns:
        ChatOpenAI: The custom LLM.
    """
    return ChatOpenAI(model_name="gpt-3.5-turbo")
