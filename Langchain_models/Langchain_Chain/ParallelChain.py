from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


load_dotenv()
model1 = ChatOpenAI()
model2 = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=1.0
)

prompt1 = PromptTemplate(
template='Generate short and simple notes from the following text \n {text}',
input_variables=['text' ]
)

prompt2 = PromptTemplate(
template='Generate 5 short question answers from the following text \n {text}',
input_variables=['text' ]
)

prompt3 = PromptTemplate(
template='Merge the provided notes and quiz into a single document. \n notes -> {notes} and quiz -> {quiz}',
input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

parallelChian = RunnableParallel({
  'notes': prompt1 | model1 | parser,
  'quiz': prompt2 | model2 | parser
})

mergeChain = prompt3 | model1 | parser
chain = parallelChian | mergeChain

text = """Machine learning (ML) is a subset of artificial intelligence that empowers systems to learn from data, identify patterns, and make decisions with minimal human intervention. Fundamentally, ML algorithms are trained on vast datasets to build a model that can then make predictions or recognize insights from new, unseen data. This process is distinct from traditional programming, where every instruction is explicitly coded. Key methodologies include supervised learning, where algorithms learn from labeled examples; unsupervised learning, which involves finding patterns in data without pre-existing labels; and reinforcement learning, where systems learn through a process of trial and error guided by a reward system. The pervasive application of machine learning spans numerous fields, driving innovations such as personalized recommendations on streaming services, accurate medical diagnoses in healthcare, fraud detection in finance, and the underlying technology for self-driving cars and advanced language models. The field continues to evolve rapidly, presenting both immense opportunities and challenges regarding ethics, bias in data, and data privacy."""

result = chain.invoke({'text': text})

print(result)

chain.get_graph().print_ascii()

