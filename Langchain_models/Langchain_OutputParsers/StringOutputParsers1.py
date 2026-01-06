from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI()

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

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser
result = chain.invoke({"topic": "Back Hole of the universe"})

print(result)