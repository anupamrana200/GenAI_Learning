
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

#Fetch YouTube transcript
video_id = "DPJSP83bTKc"

try:
    api = YouTubeTranscriptApi()
    transcript_list = api.fetch(video_id, languages=["en"])
    transcript = " ".join(item.text for item in transcript_list)

except TranscriptsDisabled:
    print("No caption available for this video")
    raise SystemExit


#Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.create_documents([transcript])


#Create embeddings + FAISS vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(chunks, embeddings)


#Retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)


#LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


#Prompt
prompt = PromptTemplate(
    template="""
You are a helpful assistant.

First, try to answer the question using ONLY the provided transcript.

If the transcript does NOT contain enough information:
- Clearly say: "The following answer is not based on the transcript."
- Then answer the question using your general knowledge.

Context (Transcript):
{context}

Question:
{question}
""",
    input_variables=["context", "question"]
)

#Ask question
question = "what is LinkedIn?"

docs = retriever.invoke(question)
context_text = "\n\n".join(doc.page_content for doc in docs)
# print(context_text)

final_prompt = prompt.invoke({
    "context": context_text,
    "question": question
})

answer = llm.invoke(final_prompt)
print(answer.content)
