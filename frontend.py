import streamlit as st
import requests
import json

st.title("Stripe AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know about your Stripe account?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create a placeholder for the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    try:
        # Prepare the conversation history
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages[:-1]  # Exclude the last user message
        ]

        # Send user input and history to FastAPI backend
        with requests.post("http://localhost:8000/chat", 
                           json={"content": prompt, "history": history}, 
                           stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    full_response += chunk.decode()
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
    
    except requests.RequestException as e:
        full_response = f"Error communicating with the server: {str(e)}"
    except Exception as e:
        full_response = f"An unexpected error occurred: {str(e)}"

    # Display the full response without the cursor
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
