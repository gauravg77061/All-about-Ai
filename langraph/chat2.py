from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional,Literal
from langgraph.graph import add_messages, StateGraph, START, END
from openai import OpenAI
import json



 


load_dotenv()
client = OpenAI()

class State(TypedDict):
    user_query:str
    llm_output: Optional[str]
    

def chatbot(state:State):
    print("chatbot",state)
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    
    state["llm_output"]=response.choices[0].message.content
    return state

def evaluate_response(state:State) -> Literal["chatbot_gemini","endNode"]:
    print("evaluate",state)
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":"Return JSON:{\"route\":\"chatbot_gemini\" or \"endNode\"}"
            },
            {
                "role":"user",
                "content":state.get("user_query")
            }
        ]
    )
    decision=json.loads(response.choices[0].message.content)
    return decision.get("route", "endNode")

def endNode(state:State):
    return state

def chatbot_gemini(state:State):
    print("gemini",state)
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    
graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endNode",endNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","endNode")
graph_builder.add_edge("endNode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"user_query":"Hey, what is 2+2"}))

print(updated_state)




