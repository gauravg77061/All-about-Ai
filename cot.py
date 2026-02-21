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
 PLAN:{"step":"PLAN":"content":"Seems like,suer is interested n maths problem"}
 PLAN:{"step:"PLAN":"content":"lloking at the problem .we should solve this problem with the help of BODMAS method"}
 PLAN:{"step":"PLAN":"Content":"we should multipy 3*5 which is 15"}
 PLAN:{"step":"PLAN":"content":"Now the equation is 2+15/10"}
  PLAN:{"step":"PLAN":"content":"we must perform divide that is equal to 1.5"}
PLAN:{"step":"PLAN":"content":"Now the equation is 2+1.5"}
PLAN:{"step":"PLAN":"content":"Now finally lets persome add 3.5"}
OUTPUT:{"step":"PLAN":"content":"Great, we have solved the problem"}

"""

response=client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey can you add n numbers in javascript "},
        #manulayy appending in chat history
        {"role":"assistant","content": json.dumps({"step":"START","content":"you want a javascript code to add n numbers"})},
        {"role":"assistant","content": json.dumps({"step": "PLAN", "content":"First, I need to clarify how the user wants to provide the n numbers, either through an array or through user input."})},
        {"role":"assistant","content": json.dumps({"step": "PLAN", "content": "Assuming the user wants to input numbers using an array, I can outline a method to use the reduce function in JavaScript."})},
        {"role":"assistant","content": json.dumps({"role":"assistant","content": json.dumps({"step":"START","content":"you want a javascript code to add n numbers"})})},
        {"role":"assistant","content": json.dumps({"step": "PLAN", "content": "I will create a function that takes an array of numbers and returns the sum."})},
        {"role":"assistant","content": json.dumps({"step": "PLAN", "content": "To implement this, I will use the Array.prototype.reduce method to sum up the numbers in the array."})},
        {"role":"assistant","content": json.dumps({"step": "PLAN", "content": "Now, I will show the user a simple code snippet for the function."})}
    ]

)
print(response.choices[0].message.content)