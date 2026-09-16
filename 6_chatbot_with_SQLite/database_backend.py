from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

load_dotenv()

# ---- Model ----
def model_name():
    return ChatOpenAI(model="gpt-4o-mini")

model = model_name()


# ---- State ----
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---- Node ----
def chat_node(state: ChatState) -> dict:
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


# ---- Graph ----
builder = StateGraph(ChatState)
builder.add_node("chat_node", chat_node)
builder.add_edge(START, "chat_node")
builder.add_edge("chat_node", END)

conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn)
chatbot = builder.compile(checkpointer=checkpointer)

def retrive_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
retrive_all_threads()