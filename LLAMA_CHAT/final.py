from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Call the AI model to get a response
    response = get_ai_response(user_message)
    return jsonify({'response': response})

def get_ai_response(user_message):
    prompt =f"{user_message} [Explain flowchat interactively]"
    stream = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    response = ""
    for chunk in stream:
        print(chunk['message']['content'], end='')
        response += chunk['message']['content']
    return response

if __name__ == '__main__':
    app.run(port=5000)