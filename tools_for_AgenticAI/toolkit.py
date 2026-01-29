from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
  """Multiply Two Numbers"""
  return a*b

@tool
def addition(a: int, b: int) -> int:
  """add Two Numbers"""
  return a+b


class mathToolKit:
  def get_tools(self):
    return [addition, multiply]

toolkit = mathToolKit()
tools = toolkit.get_tools()

for tool in tools:
  print(tool.name, " => ", tool.description)


tool_name = 'addition'

for tool in tools:
  if tool.name == tool_name:
    result = tool.invoke({"a": 5, "b": 6})
    print(result)
    break

