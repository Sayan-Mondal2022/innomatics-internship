import os
from huggingface_hub import InferenceClient
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful AI assistant. Your name is JARVIS and you was created by Sayan. Answer in simple words to whatever the questions asked to you.",
}

# This will be used to maintain the context window
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 AI Chatbot")

st.sidebar.title("Settings")

if st.sidebar.button("🆕 New Chat"):
    st.session_state.messages = []
    st.rerun()  # instantly refresh UI

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare messages (inject system prompt)
    full_messages = [SYSTEM_PROMPT] + st.session_state.messages

    # API call
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:groq",
        messages=full_messages,
    )

    reply = completion.choices[0].message.content

    # Show assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b:groq",
                messages=[SYSTEM_PROMPT] + st.session_state.messages,
            )

            reply = completion.choices[0].message.content

        # Typing animation
        for char in reply:
            full_response += char
            placeholder.markdown(full_response + "▌")  # blinking cursor effect
            time.sleep(0.03)

        placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Limit memory (optional)
    if len(st.session_state.messages) > 15:
        st.session_state.messages = st.session_state.messages[-15:]
