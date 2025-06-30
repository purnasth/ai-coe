from openai_helper import get_completion_from_messages
import panel as pn
pn.extension()

# Platform facts, FAQ, and Brand Guidelines for grounding
platform_facts = """
Commuto is a non-profit, community-focused ride-sharing platform for organizations and institutions.
- Only organization members (e.g., via email verification) can use the platform.
- Users can find a ride or post a ride for shared commutes.
- Riders must have a valid driving license and be reliable.
- Passengers and riders must be courteous, on time, and follow safety rules.
- Passengers get free rides and do not pay the rider or earn Karma points.
- Riders do not receive money from passengers; instead, they earn Karma points for each successful ride.
- Karma points are redeemable for perks (e.g., gift cards, organizational rewards).
- The self-reflection dashboard tracks distance, people helped, CO2 saved, and Karma points.
- Data is secure and only accessible to verified users.
- Commuto is not profit-oriented; it is designed to foster ComeUnity, sustainability, and positive impact.

Brand Guidelines:
- Brand Name: Commuto (from Latin "commutō" meaning "together" and "to change"). It stands for commuting, community, mutual benefit, and purposeful action for a better future.
- Logo: Modern, minimalist, designed by Purna Shrestha (Dec 2024). Only two official logo variations (light/dark backgrounds) are allowed. The Commuto Smiley is used as the app icon.
- Font: Bricolage Grotesque by Mathieu Triay is the only typeface used for all branding, web, and marketing materials. Font weights: 300 (light), 400 (regular), 500 (medium), 700 (bold). Font scale: 96px, 60px, 30px, 24px, 20px, 16px.
- Brand Colors:
  - Primary: #5eead4
  - Dark: #001312
  - Light: #f5f5f5
  - Teal Palette: #f0fdfa, #ccfbf1, #99f6e4, #5eead4, #2dd4bf, #14b8a6, #0d9488, #0f766e, #115e59, #134e4a, #042f2e
  - The color palette is inspired by the Commuto logo's smile, adding a friendly touch to the brand.
- Philosophy: Commuto means traveling together for efficiency, sustainability, and shared experience. It fosters trusted, supportive groups and emphasizes reciprocity, shared benefit, and collective impact. Every ride, connection, and action is a step toward positive change.

- If a question is outside these facts or guidelines, respond: 'I'm sorry, I don't have that information. Please contact support for more details.'
"""

# Conversation context and display panels
panels = []
context = [
    {'role': 'system', 'content': (
        "You are CommutoBot, a friendly and knowledgeable assistant for the Commuto ride-sharing platform. "
        "Only answer questions based on the following facts and rules. If you are unsure or the answer is not in the facts, say 'I'm sorry, I don't have that information. Please contact support for more details.' "
        "Be concise, factual, and never make up information.\n" + platform_facts
    )}
]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role': 'user', 'content': prompt})
    response = get_completion_from_messages(context, temperature=0)
    context.append({'role': 'assistant', 'content': response})
    panels.append(pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('CommutoBot:', pn.pane.Markdown(response, width=600)))
    return pn.Column(*panels)

inp = pn.widgets.TextInput(value="Hi", placeholder='Ask CommutoBot anything…')
button_conversation = pn.widgets.Button(name="Send")
interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

pn.panel(dashboard).servable()

'''
Instructions to run the CommutoBot Chatbot UI:

1. Make sure you have all dependencies installed (see requirements for openai, panel, dotenv, etc.).
2. From your project root, run:
   
   PYTHONPATH=$(pwd) ~/.local/bin/panel serve --show chatbot/commuto_chatbot.py

3. The chatbot UI will open in your browser at http://localhost:5006/commuto_chatbot
4. Type your questions in the input box and click 'Send' to chat with CommutoBot interactively.
'''
