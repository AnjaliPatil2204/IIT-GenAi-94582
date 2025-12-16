import streamlit as st
import time

st.title("My Chatbot")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

# Function to stream bot reply
def bot_reply_stream(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.2)

# When user sends a message
if user_input:
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Simple bot response (echo)
    bot_response = f"You said : {user_input}"

    # Display bot response using write_stream
    with st.chat_message("assistant"):
        st.write_stream(bot_reply_stream(bot_response))

    # Store bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
