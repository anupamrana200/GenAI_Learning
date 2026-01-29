from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
  """Multiply Two Numbers"""
  return a*b

result = multiply.invoke({"a": 3, "b": 5})

print(result)

print(multiply.name)
print()
print(multiply.description)
print()
print(multiply.args)