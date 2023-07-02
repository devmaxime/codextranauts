
from langchain.agents import Tool, LLMSingleActionAgent, AgentOutputParser, AgentExecutor
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re

class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

def get_custom_agent(llm: OpenAI,template: str, tools: List[Tool]):
    """
    Create a custom agent based on the template and tools provided.
    
    Parameters:
        llm (OpenAI): The LLM to use.
        template (str): The template to use.
        tools (List[Tool]): The tools to use.
        
    Returns:
        LLMSingleActionAgent: The custom agent.
    """

    # Create the prompt
    prompt = CustomPromptTemplate(
        template=template,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"]
    )

    # Create llm chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Create the agent
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=CustomOutputParser(),
        stop=["\nObservation:"],
        allowed_tools=[tool.name for tool in tools]
    )

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    return agent_executor

