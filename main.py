import streamlit as st
import time
from setup_st import *
from index_functions import generate_response_gemini

# Page setup
st.title("Rose's Prototype AI Chatbot")
set_design()
initialize_session_state()
sidebar()
clear_button()
download_button()
get_user_config()

# Ensure Gemini API key is set
api_key = st.session_state.get('api_key')
if not api_key:
    st.warning("Please enter and validate your Gemini API key in the sidebar.")
    st.stop()

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your message:"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            full_response = generate_response_gemini(
                api_key=api_key,
                prompt=prompt,
                temperature=st.session_state['temperature'],
                model=st.session_state.get('model_name', 'gemini-1.5-pro')
            )
            # Typing effect
            displayed = ""
            for word in full_response.split():
                displayed += word + " "
                message_placeholder.markdown(displayed + "▌")
                time.sleep(0.05)
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "I'm sorry, I couldn't generate a response."

    st.session_state.messages.append({"role": "assistant", "content": full_response})