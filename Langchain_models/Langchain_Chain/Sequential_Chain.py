from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenAI()

prompt1 = PromptTemplate(
  template='Generate detailed report on {topic}.',
  input_variables = ['topic']
)

prompt2 = PromptTemplate(
  template='Summarize the following report in bullet points in maximum 5 lines Here is the report: \n {report}',
  input_variables = ['report']
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'Unemployment in india'})

print(result)

chain.get_graph().print_ascii()

