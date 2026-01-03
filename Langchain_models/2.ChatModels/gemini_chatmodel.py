from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=1.0
)

result = model.invoke('if S+T=230 and S-T=200 then what is the value of S and T?')

print(result.content)