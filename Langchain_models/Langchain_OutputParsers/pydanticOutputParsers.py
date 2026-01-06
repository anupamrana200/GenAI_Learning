# from langchain_huggingface import ChatHuggingFace,  HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os

load_dotenv()

# sec_key = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

# llm = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     task="text-generation",
#     huggingfacehub_api_token=sec_key
# )

# model = ChatHuggingFace(llm=llm) 

model = ChatOpenAI()


class Person(BaseModel):
    name: str = Field(description="name of the person")
    age: int = Field(gt=18, description="age of the person")
    city: str = Field(description="city of the person")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
  template = 'Provide a name, age and city of a fictional {nationality} person.\n{format_instructions}',
  input_variables=['nationality'],
  partial_variables={'format_instructions': parser.get_format_instructions()}
)

prompt = template.invoke({'nationality': 'Indian'})
print(prompt)

result = model.invoke(prompt)

final_result = parser.parse(result.content)
print(final_result)