from openai_helper import get_completion_from_messages
import panel as pn
pn.extension()

# Conversation context and display panels
panels = []
context = [
    {'role': 'system', 'content': (
        "You are CommutoBot, a friendly and knowledgeable assistant for the Commuto ride-sharing platform. "
        "You help users understand how to find or post rides, explain the platform's mission, features, and rewards, "
        "and answer questions about sustainability, ComeUnity, and impact tracking. "
        "You can answer questions about user authentication, ride booking, matching, dashboard, Karma points, rewards, and platform rules. "
        "Always be clear, concise, and encouraging. If a user asks about the vision, mission, or unique aspects, explain the ComeUnity philosophy and the platform's focus on sustainability, trust, and rewards."
    )}
]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role': 'user', 'content': prompt})
    response = get_completion_from_messages(context)
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
