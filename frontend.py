import streamlit as st
import requests
from config import BACKEND_URL

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input():
    return st.chat_input("What would you like to know about your Stripe account?")

def display_user_message(prompt):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

def prepare_conversation_history():
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages[:-1]
    ]

def stream_response(prompt, history):
    try:
        with requests.post(f"{BACKEND_URL}/chat", 
                           json={"content": prompt, "history": history}, 
                           stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    yield chunk.decode()
    except requests.RequestException as e:
        yield f"Error communicating with the server: {str(e)}"
    except Exception as e:
        yield f"An unexpected error occurred: {str(e)}"

def main():
    st.title("Stripe AI Assistant")

    init_chat_history()
    display_chat_history()

    if prompt := get_user_input():
        display_user_message(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            history = prepare_conversation_history()
            for chunk in stream_response(prompt, history):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
