import streamlit as st
import PyPDF2
import faiss
import numpy as np
import app2  # Ensure this is the correct module

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to create FAISS index
def create_faiss_index(texts):
    embeddings = np.random.rand(len(texts), 768).astype('float32')  # Placeholder for actual embeddings
    index = faiss.IndexFlatL2(768)
    index.add(embeddings)
    return index

# Function to handle the query with Ollama
def handle_query_with_ollama(user_prompt):
    stream = app2. chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': user_prompt}],
        stream=True,
    )

    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    return response

# Streamlit app
st.title("PDF Chatbot")
st.session_state.messages = st.session_state.get('messages', [])

# PDF file uploader
pdf_file = st.file_uploader("Upload a PDF file", type='pdf')
if pdf_file:
    extracted_text = extract_text_from_pdf(pdf_file)
    # Create FAISS index for the extracted text
    faiss_index = create_faiss_index([extracted_text])  # You may want to split into chunks

# User input for querying
user_prompt = st.text_input("Ask me anything about the content of the PDF(s):")
if user_prompt:
    st.session_state.messages.append({'role': 'user', "content": user_prompt})

    # Retrieve relevant content using FAISS (This is a placeholder; implement your retrieval logic)
    relevant_context = extracted_text  # Replace this with actual retrieval logic

    # Use Ollama for querying the relevant content
    response = handle_query_with_ollama(relevant_context + "\n\n" + user_prompt)

    st.session_state.messages.append({'role': 'assistant', "content": response})

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])
