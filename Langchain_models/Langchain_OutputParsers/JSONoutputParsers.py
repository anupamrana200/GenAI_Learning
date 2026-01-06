from langchain_huggingface import ChatHuggingFace,  HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

load_dotenv()

sec_key = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=sec_key
)

model = ChatHuggingFace(llm=llm) 

parser = JsonOutputParser()

template = PromptTemplate(
  template="Provide me a name and age of a fictional person in a city.\n {format_instructions}",
  input_variables=[],
  partial_variables={"format_instructions": parser.get_format_instructions()}
)

# prompt = template.invoke({})

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)

# print(final_result)

chain = template | model | parser
result = chain.invoke({}) 
print(result)