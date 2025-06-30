import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
client = openai.OpenAI()

# List available models
models = client.models.list()
print("Available models:")
for m in models.data:
    print(m.id)

def get_completion(prompt, model="gpt-4.1-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

# ? Example usage: 1 - Generate a list of made-up book titles

# prompt = """
# Generate a list of three made-up book titles along with their authors and genres.
# Provide them in JSON format with the following keys: book_id, title, author, genre.
# """
# response = get_completion(prompt)
# print(response)

# ? Example usage: 2 - Instructions to make a cup of tea

# text_1 = f"""
# Making a cup of tea is easy! First, you need to get some \ 
# water boiling. While that's happening, \ 
# grab a cup and put a tea bag in it. Once the water is \ 
# hot enough, just pour it over the tea bag. \ 
# Let it sit for a bit so the tea can steep. After a \ 
# few minutes, take out the tea bag. If you \ 
# like, you can add some sugar or milk to taste. \ 
# And that's it! You've got yourself a delicious \ 
# cup of tea to enjoy.
# """
# prompt = f"""
# You will be provided with text delimited by triple quotes. 
# If it contains a sequence of instructions, \ 
# re-write those instructions in the following format:

# Step 1 - ...
# Step 2 - …
# …
# Step N - …

# If the text does not contain a sequence of instructions, \ 
# then simply write \"No steps provided.\"

# \"\"\"{text_1}\"\"\"
# """
# response = get_completion(prompt)
# print("Completion for Text 1:")
# print(response)

# # ? Example usage: 3 - Few shot prompting


# prompt = f"""
# Your task is to answer in a consistent style.

# <child>: Teach me about patience.

# <grandparent>: The river that carves the deepest \ 
# valley flows from a modest spring; the \ 
# grandest symphony originates from a single note; \ 
# the most intricate tapestry begins with a solitary thread.

# <child>: Teach me about resilience.
# """
# response = get_completion(prompt)
# print(response)

# ?Principle 2: Give the model time to “think”

# text = f"""
# In a charming village, siblings Jack and Jill set out on \ 
# a quest to fetch water from a hilltop \ 
# well. As they climbed, singing joyfully, misfortune \ 
# struck—Jack tripped on a stone and tumbled \ 
# down the hill, with Jill following suit. \ 
# Though slightly battered, the pair returned home to \ 
# comforting embraces. Despite the mishap, \ 
# their adventurous spirits remained undimmed, and they \ 
# continued exploring with delight.
# """
# # example 1
# prompt_1 = f"""
# Perform the following actions: 
# 1 - Summarize the following text delimited by triple \
# backticks with 1 sentence.
# 2 - Translate the summary into French.
# 3 - List each name in the French summary.
# 4 - Output a json object that contains the following \
# keys: french_summary, num_names.

# Separate your answers with line breaks.

# Text:
# ```{text}```
# """
# response = get_completion(prompt_1)
# print("Completion for prompt 1:")
# print(response)

# # ?Tactic 1: Specify the steps required to complete a task

# prompt_2 = f"""
# Your task is to perform the following actions: 
# 1 - Summarize the following text delimited by 
#   <> with 1 sentence.
# 2 - Translate the summary into French.
# 3 - List each name in the French summary.
# 4 - Output a json object that contains the 
#   following keys: french_summary, num_names.

# Use the following format:
# Text: <text to summarize>
# Summary: <summary>
# Translation: <summary translation>
# Names: <list of names in summary>
# Output JSON: <json with summary and num_names>

# Text: <{text}>
# """
# response = get_completion(prompt_2)
# print("\nCompletion for prompt 2:")
# print(response)

fact_sheet_macbook = """
OVERVIEW
- Apple MacBook Pro 14-inch (2023) with M3 chip.
- Available in Silver and Space Gray.
- Liquid Retina XDR display with ProMotion technology.
- Up to 18 hours battery life.
- Magic Keyboard with Touch ID.
- macOS Sonoma pre-installed.

PERFORMANCE
- Apple M3 chip with 8-core CPU and 10-core GPU.
- Up to 24GB unified memory.
- Up to 2TB SSD storage.

DISPLAY
- 14.2-inch (diagonal) Liquid Retina XDR display.
- 3024-by-1964 native resolution at 254 pixels per inch.
- ProMotion technology for adaptive refresh rates up to 120Hz.

PORTS
- Three Thunderbolt 4 (USB-C) ports.
- HDMI port, SDXC card slot, MagSafe 3 charging port.
- 3.5mm headphone jack.

CAMERA & AUDIO
- 1080p FaceTime HD camera.
- Six-speaker sound system with force-cancelling woofers.
- Studio-quality three-mic array.

CONNECTIVITY
- Wi-Fi 6E and Bluetooth 5.3.

DIMENSIONS & WEIGHT
- Height: 1.55 cm (0.61 inches)
- Width: 31.26 cm (12.31 inches)
- Depth: 22.12 cm (8.71 inches)
- Weight: 1.6 kg (3.5 pounds)

COUNTRY OF ORIGIN
- China
"""

prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Technical specifications: ```{fact_sheet_macbook}```
"""
response = get_completion(prompt)
print(response)