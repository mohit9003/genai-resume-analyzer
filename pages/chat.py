import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")

st.set_page_config(page_title="AI Chat", page_icon="🤖")

st.title("🤖 AI Chat Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat UI
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = model.generate_content(prompt)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(reply)