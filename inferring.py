from openai_helper import get_completion

#? Example 1: Sentiment analysis for provided review 

# lamp_review = """
# Needed a nice lamp for my bedroom, and this one had \
# additional storage and not too high of a price point. \
# Got it fast.  The string to our lamp broke during the \
# transit and the company happily sent over a new one. \
# Came within a few days as well. It was easy to put \
# together.  I had a missing part, so I contacted their \
# support and they very quickly got me the missing piece! \
# Lumina seems to me to be a great company that cares \
# about their customers and products!!
# """

# prompt = f"""
# What is the sentiment of the following product review, 
# which is delimited with triple backticks?

# Review text: '''{lamp_review}'''
# """
# response = get_completion(prompt)
# print(response)

#? Example 2: Detailed Inference Example - Extracting Multiple Attributes from a Review

# This example demonstrates how to use prompt engineering to infer multiple attributes from a product review, such as sentiment, mentioned features, and whether the reviewer recommends the product. This is a common use case in prompt engineering for extracting structured information from unstructured text.

macbook_review = """
I recently purchased the Apple MacBook Pro 14-inch (2023) with the M3 chip, and it has exceeded my expectations. The display is stunning, performance is lightning fast, and the battery lasts all day. The build quality feels premium, and the keyboard is comfortable to type on. However, I wish it had more USB-A ports. Overall, I highly recommend this laptop for professionals and students alike!
"""

prompt = f"""
Analyze the following product review (delimited by triple backticks) and extract the following information:
1. Sentiment (Positive, Negative, or Neutral)
2. List of product features mentioned (e.g., display, performance, battery, build quality, keyboard, ports)
3. For each feature, indicate if the sentiment is positive, negative, or neutral
4. Does the reviewer recommend the product? (Yes/No)
5. Output the result as a JSON object with keys: sentiment, features, feature_sentiments, recommends

Review: ```{macbook_review}```
"""
response = get_completion(prompt)
print("\nExample 2: Detailed Inference Result:")
print(response)