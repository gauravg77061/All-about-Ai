import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# print("KEY =", os.getenv("OPENAI_API_KEY"))

client=OpenAI()

#Zero prompting

SYSTEM_PROMPT="Your name is Coding Alexa.You shuld only ams coding related questions and if query is not related to coding just say sorry"

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey can you tell me about even llop in node js"}
    ]

)
print(response.choices[0].message.content)