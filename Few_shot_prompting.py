import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# print("KEY =", os.getenv("OPENAI_API_KEY"))

client=OpenAI()

SYSTEM_PROMPT="""
Your name is coding alexa and you wil ans only coding related problems 
and if queston is not related to coding just say so"

Rule:
-Strictly follow the output in Json format
{{
"code":"String or Null",
"isCodingProblem:"boolean"
}}

Examples:
Q:can you explain a+b whole square?
A:{{
"code":"null",
"isCodingProblem:"false"
}}

Q:Hey write a code in python to add two numbers
A: def add(a,b):
      return (a+b)

"""
response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey can you explain a+b whole square?"}
    ]

)
print(response.choices[0].message.content)