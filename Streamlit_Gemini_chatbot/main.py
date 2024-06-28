import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Gemini Chatbot test1", page_icon=":beers:", layout="centered"
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def translate_role_for_user(user_role):
    if user_role == "model":
        return "Assistant"
    else:
        return user_role
    
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_user(message.role)):
        st.markdown(message.parts[0].text)

st.header("Google Gemini chatbot with streamlit library")
prompt = st.chat_input("Hello..👋Have fun while chatting google ")
if prompt:
    st.chat_message("user").markdown(prompt)
    gemini_response = st.session_state.chat_session.send_message(prompt)
    with st.chat_message("Assistant"):
        st.markdown(gemini_response.text)
