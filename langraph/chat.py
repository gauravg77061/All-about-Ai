from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from openai import OpenAI

load_dotenv()

llm = OpenAI(model="gpt-4o-mini")

#Annotated -> add mesage 
# state={message :[hey there]}
# node runs: chat boat initial state -> hey there 
# than state changes to {message : hey there ,hi ,this is the message from the chat bot }



class State(TypedDict):
    messages: Annotated[list,add_messages]
    

#node creation
    
def chatbot(state:State):
    response=llm.invoke(state.get("messages"))
    return {"messages":[response]}
    

def sampleNode(state:State):
    print("\n\nInside the sample node ",state)
    return {"messages":["sample message Appended"]}   
 

# state graph kaa use karke grah builder ban raha 
#le kya raha h state 
graph_builder = StateGraph(State)

#graph ko pata nahi h koi node h we have to add it 
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sampleNode",sampleNode)

#creating edge 

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["Hi, My name is Gaurav gupta"]}))
print("\n\n updated_state",updated_state)
#jab ham graph ko invoke krte h we need to pass its initial State
#State ->initial state 
#state-> particular chat ki initial state h 







