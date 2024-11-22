import streamlit as st
import app2

st.title("Ollama Chat with LLaMA 3.2")

# Input for the user message
user_input = st.text_input("Ask a question:")

if st.button("Send"):
    if user_input:
        # Display the loading message
        response_container = st.empty()
        with response_container:
            # Stream the response
            stream = app2.chat(
                model='llama3.2',
                messages=[{'role': 'user', 'content': user_input}],
                stream=True,
            )

            # Output the streamed response
            full_response = ""
            for chunk in stream:
                full_response += chunk['message']['content']
                response_container.markdown(full_response)  # Update the response display

# Optionally add some styling
st.markdown("<style> .stTextInput { width: 100%; } </style>", unsafe_allow_html=True)
