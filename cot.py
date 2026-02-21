# Chain of thought 

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# print("KEY =", os.getenv("OPENAI_API_KEY"))

client=OpenAI()

SYSTEM_PROMPT="""
 you are an expert AI assistant in resolving query using chai of Thought 
 you work on START,PLAN< and OUTPUT steps.
 You need to first PLAN what needs to be done.The PLAN can be multiple steps.
 Once you think  enough PLAN has been done , finally you can give an OUTPUT

 Rues:
 - strictly Follow the given JSON output format
 -only run one step at a time
 - The sequence of step is START(where user given an input), PLAN (Thant can
 be multiple times) and finally OUTPUT (which is going to the the displayed to 
 the user).

 output JSON Format:
 {"step":""START|"PLAN | "Content":"String}

 Example:
 START: Hey, can you solev 2+3*5/10
 PLAN:{"step":"PLAN":"content":"Seems like,user is interested in maths problem"}
 PLAN:{"step:"PLAN":"content":"looking at the problem .we should solve this problem with the help of BODMAS method"}
 PLAN:{"step":"PLAN":"Content":"we should multiply 3*5 which is 15"}
 PLAN:{"step":"PLAN":"content":"Now the equation is 2+15/10"}
  PLAN:{"step":"PLAN":"content":"we must perform divide that is equal to 1.5"}
PLAN:{"step":"PLAN":"content":"Now the equation is 2+1.5"}
PLAN:{"step":"PLAN":"content":"Now finally lets persome add 3.5"}
OUTPUT:{"step":"PLAN":"content":"Great, we have solved the problem"}

"""

print("\n\n\n")

message_history=[
    {"role":"system","content":SYSTEM_PROMPT},

]


user_query =input("✨💬 Type your message: ")

message_history.append({"role":"user","content":user_query})

while True:
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result =(response.choices[0].message.content)
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=json.loads(raw_result)

    if parsed_result.get("step") == 'START':
        print("🔥" , parsed_result.get("content"))
        continue
    if parsed_result.get("step") == 'PLAN':
        print("🧠 ", parsed_result.get('content'))
        continue
    if parsed_result.get("step") == 'OUTPUT':
        print("🤖" , parsed_result.get("content"))
        break

print("\n\n\n")
