import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Personal Gemini ChatBot",
    page_icon="✨",
    layout="centered",
)


# ============================================================
# Load API Key
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        GEMINI_API_KEY = None

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing.")
    st.stop()


# ============================================================
# Initialize Chat History
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Header
# ============================================================

st.title("✨Personal Gemini ChatBot")
st.caption("Powered by Md.Sifat Mahmud")


# ============================================================
# Display Previous Messages
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# User Input
# ============================================================

user_prompt = st.chat_input("Ask Gemini anything...")


if user_prompt:

    # --------------------------------------------------------
    # Display User Message
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # --------------------------------------------------------
    # Create Gemini Conversation History
    # --------------------------------------------------------

    contents = []

    for message in st.session_state.messages:

        role = "model" if message["role"] == "assistant" else "user"

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ],
            )
        )

    # --------------------------------------------------------
    # Gemini API Request
    # --------------------------------------------------------

    response_text = ""

    try:

        # Create a NEW client for this request
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
        )

        response_text = response.text

        # Close client after request
        client.close()

    except Exception as e:

        response_text = f"Error: {str(e)}"

    # --------------------------------------------------------
    # Display Gemini Response
    # --------------------------------------------------------

    with st.chat_message("assistant"):
        st.markdown(response_text)

    # --------------------------------------------------------
    # Save Gemini Response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text,
        }
    )