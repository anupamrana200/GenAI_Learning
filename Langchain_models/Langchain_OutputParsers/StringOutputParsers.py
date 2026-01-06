from langchain_huggingface import ChatHuggingFace,  HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

sec_key = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=sec_key
)

model = ChatHuggingFace(llm=llm) 

#first promt for detailed report
template1 = PromptTemplate(
  template="Write a detailed report about {topic}.",
  input_variables=["topic"]
)

#second prompt for concise summary
template2 = PromptTemplate(
  template="Summarize the following text in 5 lines. \n {text}",
  input_variables=["text"]
)

prompt1 = template1.invoke({"topic": "Back Hole of the universe"})
result1 = model.invoke(prompt1)

prompt2 = template2.invoke({"text": result1.content})
result2 = model.invoke(prompt2)

print(result2.content)