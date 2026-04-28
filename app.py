import streamlit as st
from core.gemini_client import GeminiClient
from core.prompt_manager import PromptManager
from core.memory_manager import ConversationMemory
from core.response_handler import ResponseHandler
from utils.logger import get_logger

logger = get_logger()

st.set_page_config(
    page_title="Edith AI Consultation",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Edith AI Consultation")
st.caption("Firm level consultation at your firgertips")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    gemini_client = GeminiClient()
except Exception:
    st.error("❌ Gemini API Key not found. Please configure Streamlit Secrets.")
    st.stop()

prompt_manager = PromptManager()
response_handler = ResponseHandler()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about careers, skills, roadmaps, or transitions...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your career context..."):
            context = st.session_state.memory.get_context()
            prompt = prompt_manager.build_prompt(user_input, context)

            raw_response = gemini_client.generate_response(prompt)
            final_response = response_handler.process(raw_response)

            st.markdown(final_response)

            st.session_state.memory.update(user_input, final_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_response}
            )