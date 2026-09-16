import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "1"}}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="bot.png"):
            st.text(message["content"])
    else:
        with st.chat_message("assistant"):
            st.text(message["content"])
            
            
user_input = st.chat_input("Type here")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user", avatar="bot.png"):
        st.text(user_input)
    

    response = chatbot.invoke({"messages":[HumanMessage(content = user_input)]},config=CONFIG)
    ai_message = response["messages"][-1].content
    st.session_state.messages.append({"role":"assistant","content":ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)