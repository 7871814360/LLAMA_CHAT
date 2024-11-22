from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
import ollama
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return Response("No message provided", status=400)

    # Start the chat stream
    stream = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': user_message}],
        stream=True,
    )

    def generate():
        response_text = ""
        for chunk in stream:
            response_text += chunk['message']['content']
            
            # Yield when a newline is detected or a certain length is reached
            if '\n' in response_text:  # Adjust length as needed
                yield response_text.strip() + " "  # Add space for formatting
                response_text = ""

        # Send any remaining text
        if response_text:
            yield response_text.strip()

    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)