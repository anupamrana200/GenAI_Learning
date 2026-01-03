from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os

# Ensure .env is loaded
load_dotenv(find_dotenv(usecwd=True))

if not os.getenv("GOOGLE_API_KEY"):
    print("Checking env: API Key NOT found.")
else:
    print("Checking env: API Key found.")

try:
    print("Initializing ChatGoogleGenerativeAI...")
    # Use a dummy model initially
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    print(f"Client type: {type(llm.client)}")
    
    print("\nAttempting to list models using llm.client.models.list():")
    # Based on the traceback, llm.client is likely a google.genai.Client instance
    # which has a .models property with a .list() method.
    if hasattr(llm.client, "models"):
        count = 0
        for m in llm.client.models.list():
            print(f" - {m.name}")
            count += 1
            if count >= 10: break # limit output
        if count == 0:
            print("No models returned.")
    else:
        print("Client does not have 'models' attribute. Trying list_models()...")
        if hasattr(llm.client, "list_models"):
             for m in llm.client.list_models():
                print(f" - {m.name}")
        else:
            print("Cannot find list method on client.")
            print(dir(llm.client))

except Exception as e:
    print(f"Error occurred: {e}")
