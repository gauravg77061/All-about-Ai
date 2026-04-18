from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os

# Load env
load_dotenv()

# LLM
llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

# State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Node
def chatbot(state: State):
    print("chatbot:", state)

    response = llm.invoke(state["messages"])

    return {"messages": [response]}

# Graph builder
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# ✅ MongoDB Checkpointer Setup (CORRECT WAY)
def compile_graph_with_checkpointer():
    DB_URI = os.getenv("MONGO_URI")

    if not DB_URI:
        raise ValueError("MONGO_URI not found in .env")

    client = MongoClient(DB_URI)  # ✅ correct
    checkpointer = MongoDBSaver(client)  # ✅ correct

    return graph_builder.compile(checkpointer=checkpointer)

# Compile graph
graph_with_checkpointer = compile_graph_with_checkpointer()

# ✅ Config (VERY IMPORTANT)
config = {
    "configurable": {
        "thread_id": "Gaurav"   # unique user/session id
    }
}

# Invoke graph
for chunk in graph_with_checkpointer.stream(
    {"messages": ["Hi,can u telme the name "]},
    config=config,   # ✅ MUST
    stream_mode="values"
    ):
    chunk["messages"][-1].pretty_print()
    


