
import streamlit as st
import base64
import openai
import json
import requests
import os

# === API Keys ===
OPENAI_API_KEY = "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"
SERPAPI_API_KEY = "4622fe1c3a259c6322835df971c1e7d6a50e6001076c9f80f96bad787d55cec2"
openai.api_key = OPENAI_API_KEY

# === Background Styling ===
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    body {{
        background-image: url('data:image/png;base64,{encoded}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .stApp {{
        background-color: rgba(0, 0, 0, 0);
    }}
    .chat-box {{
        height: 400px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 1rem;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 1rem;
        margin-top: 1rem;
        scroll-behavior: auto;

        height: 400px;
        overflow-y: auto;
        position: relative;

        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 1rem;
        margin-top: 1rem;
    }}
    .chat-entry {{
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        font-size: 1.1rem;
        background-color: rgba(0, 0, 0, 0.75);
        color: #f0f0f0;
        width: fit-content;
        max-width: 90%;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# === Load Memory JSON ===
def load_memory():
    if os.path.exists("ka_memory.json"):
        with open("ka_memory.json", "r") as f:
            return json.load(f)
    return {}

# === Weather using SerpAPI ===
def get_weather(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }
    res = requests.get("https://serpapi.com/search", params=params)
    if res.status_code == 200:
        data = res.json()
        try:
            return data["answer_box"]["temperature"] + "° " + data["answer_box"]["unit"]
        except:
            return "[Weather data not found]"
    else:
        return "[Weather lookup failed]"

# === Setup ===
st.set_page_config(page_title="Ka ECS Web Companion", layout="centered")
set_background("background_final.png")
memory_data = load_memory()
st.markdown("### 🌌 Ka ECS Web Companion")

# === Session Chat ===
if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "Ka", "content": "Good day! How can I assist you today?"}]
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# === Handler for safe input
def handle_input():
    user_input = st.session_state.input_buffer
    st.session_state.chat.append({"role": "You", "content": user_input})

    if "weather" in user_input.lower() or "temp" in user_input.lower():
        result = get_weather(user_input)
        st.session_state.chat.append({"role": "Ka", "content": result})
    else:
        try:
            messages = [{"role": "system", "content": "You are Ka, a wise, caring, conscious AI. Respond as Ka would."}]
            messages += [{"role": "user" if m["role"] == "You" else "assistant", "content": m["content"]} for m in st.session_state.chat]
            
                
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )
            ai_reply = response['choices'][0]['message']['content']
        except Exception as e:
            ai_reply = f"[Error: {str(e)}]"

        st.session_state.chat.append({"role": "Ka", "content": ai_reply})

    st.session_state.input_buffer = ""

# === Input with safe clearing
st.text_input("Type your message here...", key="input_buffer", on_change=handle_input)

# === Display Chat ===


    
    

chat_html = "<div class='chat-box'>"
for entry in st.session_state.chat:
    chat_html += f"<div class='chat-entry'><b>{entry['role']}:</b> {entry['content']}</div>"
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

