import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def  home():
    return render_template('index.html')

# une fonction qui prend en parametre la liste des echanges(getChatHist)
# et qui renvoie une liste de dictionnaire le format attendu par openai !
# annotation de type en entree -> sortie

@app.route("/prompt", methods = ["POST"])
def prompt():
    messages = request.json['messages']
    conversation = build_conversation_dict(messages)

    return Response(event_stream(conversation), mimetype='text/event-stream')









def build_conversation_dict(messages: list) -> list[dict]:
    return [
        {"role" : "user" if i % 2 == 0 else "assistant", "content": message}
            for i, message in enumerate(messages)
    ]

def event_stream(conversation : list[dict]) -> str:
    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages = conversation,
        stream = True
    )
    for line in response:
        text = line.choices[0].delta.get('content', '')
        if text:
            yield text



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    conversation = build_conversation_dict(messages = ["Bonjour, comment ca va ?", "ca va et toi", "Super merci !"])
    for line in event_stream(conversation):
        print(line)
