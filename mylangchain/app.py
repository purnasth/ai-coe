from langchain_helper import get_langchain_chat_response

if __name__ == "__main__":
    prompt = "how are you?"
    response = get_langchain_chat_response(prompt)
    print(response)
