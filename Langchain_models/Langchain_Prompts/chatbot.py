from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatOpenAI(model_name="gpt-4", temperature=0.9)


chathistory = [
    SystemMessage(content="You are a helpful assistant. Who have enourmus knowledge about technical stuff.")
]
while True:
    user_input = input("You: ")
    chathistory.append(HumanMessage(content=user_input))
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break

    response = model.invoke(chathistory)
    chathistory.append(response.content)
    print("Chatbot:", response.content)

print(chathistory)
