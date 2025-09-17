import streamlit as st
from openai import OpenAI
from pathlib import Path

# 1. Page layout and design
def set_design():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Build a path relative to this file
        logo_path = Path(__file__).parent / "logo.jpg"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.warning(f"Logo not found at {logo_path}")
    
    st.markdown(
        "<p style='text-align: center; font-size: 30px;'><b>[Rose's AI Chatbot]</b></p>",
        unsafe_allow_html=True
    )

# 2. Initialize session state variables
def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Hi there, what can I help you with today?"}
        ]
    if 'message_count' not in st.session_state:
        st.session_state['message_count'] = 0
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = "gpt-3.5-turbo"
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.7
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = ""
    if 'use_index' not in st.session_state:
        st.session_state['use_index'] = False
    if 'openai_client' not in st.session_state:
        st.session_state['openai_client'] = None

# 3. Sidebar header
def sidebar():
    st.sidebar.markdown(
        "<h1 style='color: black; font-size: 24px;'>Chatbot Configuration</h1>",
        unsafe_allow_html=True
    )

# 4. Clear conversation button
def clear_button():
    if st.sidebar.button("Clear Conversation"):
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Hi there, what can I help you with today?"}
        ]
        st.session_state['message_count'] = 0

# 5. Prepare conversation for download
def download_convo():
    if 'messages' in st.session_state and st.session_state['messages']:
        return "\n".join(
            f"\n{'-'*20}\nRole: {msg['role']}\n{'-'*20}\n{msg['content']}\n"
            for msg in st.session_state['messages']
        )
    else:
        st.warning("There aren't enough messages to download. Please refresh the page.")
        return ""

# 6. Download conversation button
def download_button():
    full_conversation = download_convo()
    st.sidebar.download_button(
        label="Download conversation",
        data=full_conversation,
        file_name='conversation.txt',
        mime='text/plain'
    )

# 7. User configuration (API key & settings)
def get_user_config():
    st.sidebar.markdown("<b style='color: darkgreen;'>Enter OpenAI API Key:</b>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("", type="password", label_visibility="collapsed")

    if st.sidebar.button("Test API Key") and api_key:
        try:
            client = OpenAI(api_key=api_key)
            # Simple test call
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Test"}]
            )
            st.sidebar.success("API key is valid!")
            st.session_state['openai_client'] = client
            st.session_state['api_key'] = api_key
        except Exception as e:
            st.sidebar.error(f"API key invalid: {e}")
