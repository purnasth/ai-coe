from openai_helper import get_completion, get_completion_from_messages

# def chat(user_message):
#     prompt = f"You are a helpful assistant. Respond to the user's message:\nUser: {user_message}\nAssistant:"
#     response = get_completion(prompt)
#     return response

# # Example usage:
# if __name__ == "__main__":
#     user_input = "Can you recommend a good laptop for programming?"
#     print(chat(user_input))

# ? Example usage: 1 - Simple Chatbot Interaction
# messages =  [  
# {'role':'system', 'content':'You are friendly chatbot.'},    
# {'role':'user', 'content':'Hi, my name is Purna'}  ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)

# ? Example usage: 2 - Chatbot with User Query
# messages =  [  
# {'role':'system', 'content':'You are friendly chatbot.'},    
# {'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)

# ? Example usage: 3 - Chatbot with User Query and Assistant Response
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Purna'},
{'role':'assistant', 'content': "Hi Purna! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)