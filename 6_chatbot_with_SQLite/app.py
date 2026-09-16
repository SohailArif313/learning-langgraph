import uuid
import streamlit as st
from database_backend import chatbot,retrive_all_threads
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="AI Workspace", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0E1117; }
.stButton>button { border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)


def new_id():
    return str(uuid.uuid4())


def add_thread(tid, title="New Conversation"):
    st.session_state.chat_threads.setdefault(tid, title)


def load_conversation(tid):
    try:
        msgs = chatbot.get_state({"configurable": {"thread_id": tid}}).values.get("messages", [])
        return [{"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content} for m in msgs]
    except Exception:
        return []


def reset_chat():
    st.session_state.thread_id = new_id()
    st.session_state.messages = []


st.session_state.setdefault("messages", [])
st.session_state.setdefault("thread_id", new_id())
st.session_state.setdefault("messages", [])
st.session_state.setdefault("thread_id", new_id())

if "chat_threads" not in st.session_state:
    st.session_state.chat_threads = {}
    for tid in retrive_all_threads():
        msgs = load_conversation(tid)
        title = msgs[0]["content"][:26] + "..." if msgs else "New Conversation"
        st.session_state.chat_threads[tid] = title

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("⚡ AI Workspace")
    if st.button("➕ New Chat", type="primary"):
        reset_chat()
        st.rerun()

    st.markdown("### 💬 Recent Chats")
    for tid, title in list(st.session_state.chat_threads.items())[::-1]:
        label = ("📌 " if tid == st.session_state.thread_id else "💭 ") + title
        if st.button(label, key=tid):
            st.session_state.thread_id = tid
            st.session_state.messages = load_conversation(tid)
            st.rerun()

# ---------------- Chat Area ----------------
st.markdown("## Chat Assistant")

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    if st.session_state.thread_id not in st.session_state.chat_threads:
        title = user_input[:26] + ("..." if len(user_input) > 26 else "")
        add_thread(st.session_state.thread_id, title)

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
            ai_message = response["messages"][-1].content
            st.markdown(ai_message)

    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    st.rerun()