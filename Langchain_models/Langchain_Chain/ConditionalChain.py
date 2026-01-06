from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()
model = ChatOpenAI()
parser = StrOutputParser()

class feedbackModel(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description="The sentiment of the review, either 'positive' or 'negative'")

parser2 = PydanticOutputParser(pydantic_object=feedbackModel)

prompt1 = PromptTemplate(
  template='Classify the sentiment of the following review as positive or negative. \n{feedback} \n {format_instructions}',
  input_variables=['feedback'],
  partial_variables={'format_instructions': parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

# result = classifier_chain.invoke({'Review': "The product quality is outstanding and exceeded my expectations!"})
# print(result.sentiment)

prompt2 = PromptTemplate(
    template = 'Write a appropriate response for the positive feedback.\n {feedback}',
    input_variables = ['feedback']
)

prompt3 = PromptTemplate(
    template = 'Write a appropriate response for the negative feedback.\n {feedback}',
    input_variables = ['feedback']
)

branch_chain = RunnableBranch(
(lambda x:x. sentiment == 'positive', prompt2 | model | parser),
(lambda x:x. sentiment == 'negative', prompt3 | model | parser),
RunnableLambda(lambda x: "could not find sentiment")
)

chain = classifier_chain | branch_chain

print(chain. invoke({'feedback': 'This is a terrible phone'}))


