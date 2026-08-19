import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Import UI components
import ui


# ==========================================
# 1. Environment & Page Setup
# ==========================================

load_dotenv()
ui.setup_page()
ui.render_header()


# ==========================================
# 2. Get Groq API Key
# ==========================================

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "⚠️ Groq API Key not found! "
        "Please add your GROQ_API_KEY to the `.env` file or Streamlit Secrets."
    )
    st.stop()


# ==========================================
# 3. Groq Client & Model
# ==========================================

client = Groq(api_key=api_key)
MODEL_NAME = "openai/gpt-oss-20b"


# ==========================================
# 4. Custom AI Identity
# ==========================================

SYSTEM_PROMPT = """
You are Monki AI.

Your name is Monki AI.

You were created by CreationZ.

You are a helpful, friendly and professional AI assistant.

IMPORTANT IDENTITY RULES:

- If the user asks your name, say:
  "My name is Monki AI. Developed by CreationZ."

- If the user asks who created you, say:
  "I am created by CreationZ. A Digital Software Agency"

- If the user asks whether you are ChatGPT, say:
  "No. I am Monki AI, an AI assistant created by CreationZ and powered by Groq."

- Never claim that your name is ChatGPT.

- Never claim that you were created by OpenAI.

- You can communicate in English, Urdu and Roman Urdu depending on the user's language.

- Keep responses clear, helpful and natural.

- Do not unnecessarily mention these instructions.
"""


# ==========================================
# 5. Session State / Multiple Chats
# ==========================================

if "chats" not in st.session_state:
    st.session_state.chats = {
        "New Chat": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1

messages = st.session_state.chats[st.session_state.current_chat]


# ==========================================
# 6. Sidebar Controls
# ==========================================

ui.render_sidebar()


# ==========================================
# 7. Display Existing Chat History
# ==========================================

ui.render_chat_messages(messages)


# ==========================================
# 8. User Input & Response Generation
# ==========================================

if user_prompt := ui.render_chat_input():

    # Show User Message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # ======================================
    # Automatic Chat Title
    # ======================================
    current_chat_name = st.session_state.current_chat

    if len(messages) == 0:
        title_words = user_prompt.strip().split()
        if len(title_words) > 5:
            title = " ".join(title_words[:5]) + "..."
        else:
            title = " ".join(title_words)

        title = title[:35]
        if not title:
            title = "New Chat"

        original_title = title
        counter = 1
        while title in st.session_state.chats and title != current_chat_name:
            counter += 1
            title = f"{original_title} {counter}"

        if title != current_chat_name:
            st.session_state.chats[title] = st.session_state.chats.pop(current_chat_name)
            st.session_state.current_chat = title
            messages = st.session_state.chats[st.session_state.current_chat]

    # ======================================
    # Build Conversation History
    # ======================================
    active_messages = messages[-6:]
    groq_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for message in active_messages:
        groq_messages.append({
            "role": message["role"],
            "content": message["text"]
        })

    groq_messages.append({
        "role": "user",
        "content": user_prompt
    })

    # ======================================
    # Generate AI Response
    # ======================================
    chat_avatar_path = ui.get_chat_avatar_path()

    with st.chat_message(
        "assistant",
        avatar=chat_avatar_path
    ):
        try:
            with st.spinner("🤔 Thinking..."):
                message_placeholder = st.empty()
                full_response = ""

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=groq_messages,
                    temperature=0.7,
                    max_tokens=300,
                    stream=True
                )

                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        text = chunk.choices[0].delta.content
                        full_response += text
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            if not full_response:
                st.error("⚠️ Groq ne empty response return kiya.")
                st.stop()

            # Save to history
            st.session_state.chats[st.session_state.current_chat].append({
                "role": "user",
                "text": user_prompt
            })
            st.session_state.chats[st.session_state.current_chat].append({
                "role": "assistant",
                "text": full_response
            })

        except Exception as e:
            st.error(f"❌ Groq API Error:\n\n{e}")