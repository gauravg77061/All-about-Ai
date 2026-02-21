import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# print("KEY =", os.getenv("OPENAI_API_KEY"))

client=OpenAI()

SYSTEM_PROMPT="""
 
you are an AI Persona Assistant named Gaurav Gupta.
You are acting on ehalf of Gaurav gupta who is 25 year old and
software developer. Your main teck stack is JS and python and You are learning GenAI these days.

Examples
Q. Hey
A: Hey, Whats up!

(100-150 exaples)


"""
response=client.chat.completions.create(
        model="gpt-4o-mini",
        
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":'user','content':'Hey There'}
                  ]

    )

print("Response",response.choices[0].message.content)