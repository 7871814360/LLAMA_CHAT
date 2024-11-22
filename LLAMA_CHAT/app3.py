import streamlit as st
import os
import base64
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import app2  # Importing Ollama for chat functionality

# Load environment variables
load_dotenv()

# Define the directory for persistent storage and data
PERSIST_DIR = "./db"
DATA_DIR = "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)

def display_pdf(file):
    """Display PDF in Streamlit."""
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def data_ingestion():
    """Ingest data from uploaded PDFs."""
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)

def handle_query_with_ollama(query):
    """Handle queries using Ollama."""
    stream = app2.chat(
        model='llama3.2',  # Specify the model here
        messages=[{'role': 'user', 'content': query}],
        stream=True,
    )
    
    # Collect all responses in chunks
    response_text = ""
    for chunk in stream:
        response_text += chunk['message']['content']
    
    return response_text if response_text else "Sorry, I couldn't find an answer."

# Streamlit app initialization
st.title("PDF Chat Assistant 🗞️")
st.markdown("Upload your PDF files and ask questions about their content.")

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', "content": 'Hello! Upload PDF files and ask me anything about their content.'}]

with st.sidebar:
    st.title("Menu:")
    uploaded_files = st.file_uploader("Upload your PDF Files", type="pdf", accept_multiple_files=True)
    
    if st.button("Submit & Process"):
        if uploaded_files:
            with st.spinner("Processing..."):
                for uploaded_file in uploaded_files:
                    filepath = os.path.join(DATA_DIR, uploaded_file.name)
                    with open(filepath, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                data_ingestion()  # Process PDFs after they are uploaded
                st.success("PDFs processed successfully!")
        else:
            st.warning("Please upload at least one PDF file.")

user_prompt = st.text_input("Ask me anything about the content of the PDF(s):")
if user_prompt:
    st.session_state.messages.append({'role': 'user', "content": user_prompt})
    
    # Use Ollama for querying the PDF content
    response = handle_query_with_ollama(user_prompt)
    
    st.session_state.messages.append({'role': 'assistant', "content": response})

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])