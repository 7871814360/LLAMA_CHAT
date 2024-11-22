import ollama

stream = ollama. chat(
model='llama3.2',
messages=[{'role': 'user', 'content': 'Question :Simple python Program to add two numbers '}],
stream=True
)
# print(stream)
for chunk in stream:
    print(chunk['message'] ['content'], end='')