from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
  template = "Wrtie a summery about the following poem.\n {poem}",
  input_variables = ["poem"],
)

parser = StrOutputParser()

loader = TextLoader('cricket.txt', encoding='utf8')

docs = loader.load()

chain = prompt | model | parser
result = chain.invoke({'poem':docs[0].page_content})
print(result)