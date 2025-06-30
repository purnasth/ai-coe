from openai_helper import get_completion

# ? Example usage: 1 - Translate a text
# prompt = f"""
# Translate the following English text to Spanish: \ 
# ```Hi, I would like to order a blender```
# """
# response = get_completion(prompt)
# print(response)

# ? Example usage: 2 - Identify the language of a text
# prompt = f"""
# Tell me which language this is: 
# ```मेरो नाम पूर्ण हो। ```
# """
# response = get_completion(prompt)
# print(response)

# ? Example usage: 3 - Universal Translator


user_messages = [
  "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
  "Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
  "Il mio mouse non funziona",                                 # My mouse is not working
  "Mój klawisz Ctrl jest zepsuty",                             # My keyboard has a broken control key
  "我的屏幕在闪烁"                                               # My screen is flashing
] 

for issue in user_messages:
    prompt = f"Tell me what language this is: ```{issue}```"
    lang = get_completion(prompt)
    print(f"Original message ({lang}): {issue}")

    prompt = f"""
    Translate the following  text to English \
    and Korean: ```{issue}```
    """
    response = get_completion(prompt)
    print(response, "\n")