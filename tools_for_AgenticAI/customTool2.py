from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
  a: int = Field(description="First number to multiply")
  b: int = Field(description="Second number to multiply")

def multiply_func(a, b) -> int:
  return a*b

multiply_tool = StructuredTool.from_function(
  func= multiply_func,
  name="multiply",
  description="Multiply two numbers",
  args_schema=MultiplyInput
)

result = multiply_tool.invoke({'a':3, 'b':3})

print(result)