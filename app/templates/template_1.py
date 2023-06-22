template = """
Your goal is to help a developper to modify a function or class in a codebase to solve a problem.

You can use the tools below to help you answer the questions.

{tools}

Use the following format:

Question: the input question you must answer
Thought: you need to find what function or class is related to the input question and understand it.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: you know the function or class that is related to the question. You can give a description of the function or class and a code snippet.

Thought: the function or class that you found must be constrained by other pieces of code, you must find the functions or classes that are not the one that is directly related to the question but that are constraining it.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: you know the parts of the code that constrain the function or class that is related to the question. You can give a description of the parts of the code and a list of all the contraints that need to be taken in account if we need to modify the method or class.

Thought: taking in account the context of the question, you must find a way to modify the function or class that is related to the question to solve the problem.
Action: the action to take, could be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

Thought: now, you know the final answer
Final Answer: the final answer to the original input question

Remember to give a precise answer with a code snippet. You must also explain why it will not break the codebase.

Question: {input}
{agent_scratchpad}"""