from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

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

checkpointer = MemorySaver()
chatbot = builder.compile(checkpointer=checkpointer)