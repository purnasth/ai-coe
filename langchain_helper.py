from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

# Get the OpenAI API key from environment variables
key = os.getenv("OPENAI_API_KEY")

# Default model can be changed as needed
def get_langchain_chat_response(prompt, model="gpt-4.1-nano"):
    chat_model = ChatOpenAI(api_key=key, model=model)
    response = chat_model.invoke(prompt)
    return response.content
