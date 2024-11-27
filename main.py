import streamlit as st
import time
from setup_st import *
from index_functions import generate_response_openai

# Set up the page
st.title("Rose's Prototype AI Chatbot")
set_design()
initialize_session_state()
sidebar()
clear_button()
download_button()
get_user_config()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get OpenAI client from session state
client = st.session_state.get('openai_client')

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input and generate response
if prompt := st.chat_input("Enter your message:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Generate a response
            full_response = generate_response_openai(
                client=client,
                prompt=prompt,
                temperature=0.7,
                model="gpt-3.5-turbo"
            )
            # Typing effect
            for chunk in full_response.split():
                time.sleep(0.05)
                message_placeholder.markdown(chunk + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "I'm sorry, I couldn't generate a response."

    st.session_state.messages.append({"role": "assistant", "content": full_response})