from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model_name="gpt-4", temperature=0.9,max_completion_tokens=100)

result = model.invoke("write a story about india?")
print(result.content)

