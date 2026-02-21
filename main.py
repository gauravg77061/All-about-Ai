import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# print("KEY =", os.getenv("OPENAI_API_KEY"))

client=OpenAI()

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":"You are an expert in Ai and only and only ans coding related questions. That if query is not related to coding .Just say sorry and don not ans it"},
        {"role":"user","content":"Hey can solve a maths problem for me deac"}
    ]

)
print(response.choices[0].message.content)