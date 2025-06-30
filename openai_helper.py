import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
client = openai.OpenAI()

def get_completion(prompt, model="gpt-4.1-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content
