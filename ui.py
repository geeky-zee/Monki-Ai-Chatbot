import os
import streamlit as st
from PIL import Image

# ==========================================
# Base Directory Setup
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# Robust Image Path Resolver (Auto-Detect)
# ==========================================
def find_image(filename_query):
    search_dirs = [
        os.path.join(BASE_DIR, "assets"),
        BASE_DIR,
        os.path.join(os.getcwd(), "assets"),
        os.getcwd()
    ]
    clean_target = filename_query.lower().replace(" ", "").replace("_", "").replace("-", "")
    target_name_no_ext = os.path.splitext(clean_target)[0]

    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
        direct = os.path.join(directory, filename_query)
        if os.path.exists(direct):
            return direct
        try:
            for item in os.listdir(directory):
                item_clean = item.lower().replace(" ", "").replace("_", "").replace("-", "")
                if item_clean.startswith(target_name_no_ext) and any(item.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".ico"]):
                    return os.path.join(directory, item)
        except Exception:
            pass
    return None


def get_main_logo():
    return find_image("Monki Ai.png")


def get_chat_avatar_path():
    return find_image("Monki Chat.png")


# ==========================================
# 1. Page Setup & Styling
# ==========================================
def setup_page():
    chat_avatar_path = get_chat_avatar_path()
    favicon_img = "🤖"
    if chat_avatar_path:
        try:
            favicon_img = Image.open(chat_avatar_path)
        except Exception:
            favicon_img = "🤖"

    st.set_page_config(
        page_title="Monki AI",
        page_icon=favicon_img,
        layout="centered"
    )

    st.markdown(
        """
        <style>
        /* 1. Hide Streamlit Cloud Header, GitHub toolbar & Footer */
        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        #MainMenu,
        footer,
        [data-testid="stFooter"],
        div[class*="viewerBadge"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 2. Container Padding & Mobile Safe Spacing (Fixes Top Cut) */
        .block-container {
            padding-top: 2rem !important;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 3.8rem !important; /* Safe margin for Mobile / iPhone top */
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            h1 {
                font-size: 24px !important;
            }

            [data-testid="stChatMessage"] {
                padding-left: 0.2rem;
                padding-right: 0.2rem;
            }

            [data-testid="stChatInput"] {
                width: 100%;
            }

            section[data-testid="stSidebar"] {
                width: 80% !important;
            }
        }

        /* 3. Sidebar Collapse Button at Bottom End */
        [data-testid="stSidebarHeader"] {
            display: flex !important;
            visibility: visible !important;
            position: absolute !important;
            bottom: 8px !important;
            right: 12px !important;
            z-index: 1000 !important;
            padding: 0 !important;
            margin: 0 !important;
            background: transparent !important;
        }

        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] button {
            display: flex !important;
            visibility: visible !important;
        }

        /* Closed State: Toggle Button placed at bottom left */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            position: fixed !important;
            bottom: 12px !important;
            left: 12px !important;
            top: auto !important;
            z-index: 99999 !important;
        }

        /* 4. Full-height Sidebar Layout */
        section[data-testid="stSidebar"] {
            position: relative !important;
            height: 100vh !important;
            overflow: hidden !important;
            padding-top: 0 !important;
        }

        section[data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
        section[data-testid="stSidebar"] .block-container,
        [data-testid="stSidebarContent"] {
            padding-top: 0.5rem !important;
            padding-bottom: 2.2rem !important;
            height: 100vh !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            box-sizing: border-box !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:first-child {
            flex-grow: 1 !important;
            overflow-y: auto !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:last-child {
            margin-top: auto !important;
            padding-bottom: 0.2rem !important;
        }

        /* Compact Sidebar Typography */
        section[data-testid="stSidebar"] h2 {
            font-size: 1.15rem !important;
            margin: 0.2rem 0 !important;
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] h3 {
            font-size: 0.95rem !important;
            margin: 0.2rem 0 !important;
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] hr {
            margin: 0.35rem 0 !important;
        }

        section[data-testid="stSidebar"] p {
            margin: 0.1rem 0 !important;
            font-size: 0.85rem !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            padding: 0.25rem 0.5rem !important;
            min-height: auto !important;
            font-size: 0.9rem !important;
        }

        /* 5. Chat Avatar Styling */
        [data-testid="stChatMessageAvatarCustom"],
        [data-testid="stChatMessageAvatar"] {
            width: 44px !important;
            height: 44px !important;
            min-width: 44px !important;
            min-height: 44px !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        [data-testid="stChatMessageAvatarCustom"] img,
        [data-testid="stChatMessageAvatar"] img {
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important;
            background-color: transparent !important;
            border-radius: 6px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 2. Header
# ==========================================
def render_header():
    logo = get_main_logo()

    col_logo, col_title = st.columns(
        [0.10, 0.90],
        gap="small",
        vertical_alignment="center"
    )

    with col_logo:
        if logo and os.path.exists(logo):
            st.image(logo, width=65)
        else:
            st.write("🤖")

    with col_title:
        st.markdown(
            """
            <h1 style="margin:0; padding:0; font-size:2.05rem; font-weight:700; line-height:1.2;">
                Meet Monki — Your AI Companion
            </h1>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <p style="margin-top:2px; margin-bottom:18px; color:rgba(250, 250, 250, 0.6); font-size:0.875rem;">
            Developed by CreationZ | Custom Ai ChatBot
        </p>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 3. Sidebar Controls
# ==========================================
def render_sidebar():
    logo = get_main_logo()

    with st.sidebar:
        with st.container():
            if logo and os.path.exists(logo):
                st.image(logo, width=75)

            st.header("⚙️ Session Controls")

            if st.button("＋ New Chat", use_container_width=True):
                st.session_state.chat_counter += 1
                new_chat = "New Chat"

                if new_chat in st.session_state.chats:
                    new_chat = f"New Chat {st.session_state.chat_counter}"

                st.session_state.chats[new_chat] = []
                st.session_state.current_chat = new_chat
                st.rerun()

            st.subheader("Recent Chats")

            for chat_name in list(st.session_state.chats.keys()):
                if st.button(
                    f"💬 {chat_name}",
                    key=f"chat_button_{chat_name}",
                    use_container_width=True
                ):
                    st.session_state.current_chat = chat_name
                    st.rerun()

        with st.container():
            st.divider()

            messages = st.session_state.chats.get(st.session_state.current_chat, [])

            st.write(f"Current Chat: **{st.session_state.current_chat}**")
            st.write(f"Total Messages: {len(messages)}")

            if st.button("🧹 Clear Chat History", use_container_width=True):
                st.session_state.chats[st.session_state.current_chat] = []
                st.rerun()

            if st.button("🗑️ Delete Chat", use_container_width=True):
                if st.session_state.current_chat in st.session_state.chats:
                    del st.session_state.chats[st.session_state.current_chat]

                if not st.session_state.chats:
                    st.session_state.chats = {"New Chat": []}
                    st.session_state.current_chat = "New Chat"
                else:
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

                st.rerun()


# ==========================================
# 4. Chat Messages Render
# ==========================================
def render_chat_messages(messages):
    chat_avatar = get_chat_avatar_path()

    for message in messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["text"])
        else:
            with st.chat_message("assistant", avatar=chat_avatar):
                st.markdown(message["text"])


# ==========================================
# 5. Chat Input
# ==========================================
def render_chat_input():
    return st.chat_input("Ask Anything...")