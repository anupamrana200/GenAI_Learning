from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests

load_dotenv()

#Tool Create
@tool
def multiply(a: int, b: int) -> int:
  """give two numbers a and b and the tool can return their product."""
  return a*b


#tool binding
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools([multiply])

# result = llm_with_tools.invoke("what is the multiplication of 3 and 4?")

# # result1 = multiply.invoke(result.tool_calls[0]['args'])
# result1 = multiply.invoke(result.tool_calls[0])
# print(result1)


query = HumanMessage("what is the multiplication of 3 and 4?")
messages = [query]

AIreply = llm_with_tools.invoke(messages)
messages.append(AIreply)

tool_result = multiply.invoke(AIreply.tool_calls[0])
messages.append(tool_result)


result = llm_with_tools.invoke(messages)
# print(result)
print(result.content)

