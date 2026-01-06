from langchain_huggingface import ChatHuggingFace,  HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
import os

load_dotenv()

sec_key = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=sec_key
)

model = ChatHuggingFace(llm=llm) 


schema = [
  ResponseSchema(name = 'Fact1', description = 'Fact 1 about the topic'),
  ResponseSchema(name = 'Fact2', description = 'Fact 2 about the topic'),
  ResponseSchema(name = 'Fact3', description = 'Fact 3 about the topic')
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
  template='Provide 3 interesting facts about {topic} in the following format: \n {format_instructions}',
  input_variables=['topic'],
  partial_variables={'format_instructions': parser.get_format_instructions()}
)

prompt = template.invoke({'topic': 'Back Hole of the universe'})
result = model.invoke(prompt)

final_result = parser.parse(result.content)
print(final_result)