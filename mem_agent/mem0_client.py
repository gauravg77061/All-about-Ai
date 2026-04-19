from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI

import os
import json


load_dotenv()

client=OpenAI()

OPEN_API_KEY=os.getenv("OPEN_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_PATH = os.path.join(BASE_DIR, "faiss_db")
os.makedirs(FAISS_PATH, exist_ok=True)

config={
    "version":"v1.1",
    "embedder": {
        "provider":"openai",
        "config":{"api_key":OPEN_API_KEY,"model":"text-embedding-3-small"}
    },
    
    "llm":{
        "provider":"openai",
        "config":{"api_key":OPEN_API_KEY,"model":"gpt-4.1"}
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url":"neo4j+s://c7bf4556.databases.neo4j.io",
            
            "username":"c7bf4556",
            "password":"s-eQh8kcQowhhmwPw1INYXvmgEOD0rGPdxfqJCbw6Sc"
        }
    },
    "vector_store":{
        "provider":"faiss",
        "config":{
            "collection_name":"memory_db",
            "path":FAISS_PATH
        }
        
    }
}

#memorymein config pass kar do
# by using config 
# by using this mem_ client 
# we can add and query your mem

mem_client=Memory.from_config(config)

while True:
    

    user_query=input(">")
    
    if user_query.lower() == "exit":
        break
    
    # it will give the dict of relevant data 
    
    search_memory=mem_client.search(query=user_query,filters={"user_id":"Gaurav"})
    
    memory_about_user=search_memory
    
    #separating only memories
    
    memories=[
        f"ID:{mem.get('id')}\nMemory: {mem.get('memory')}" 
        for mem in search_memory.get("results")
    ]
    
    #printing these memories
    # print("Found Memories",memories)
    
    #passing these memories as a system prompt 
    
    SYSTEM_PROMPT=f""" 
        here is the context abut the user:
        {json.dumps(memories)}
    """
    
    

    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_query}
        ]
    )
    ai_response=response.choices[0].message.content

    print("AI",ai_response)

    mem_client.add(
        
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":ai_response}
        ],
        # this is important 
        user_id="Gaurav"
    )

    print("Memory has been saved ....")
    
    # step to 
    # first install memoai
    # insatll fassi
    # than do the configuraton of embeddingsa ll and vector db
    # make one insatnce from mem0
    # than add that instace by using add method
    # than run the file and give the prompt to the llm
    # than u can find the reqquired data unser memory_json.file
    
    
    # 2nd step
    
    # searching the relevant memory  by mem_client.search
    # than fetching the memory because it si stored in dict form
    # than passing those relevant info as a system prompt




    







