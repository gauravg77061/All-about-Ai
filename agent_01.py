from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel,Field
from typing import Optional



load_dotenv()

client=OpenAI()

SYSTEM_PROMPT="""

Your are an expert Ai agent in resolving user queries using 
chai of thought.
you work on START,PLAN and OUTPUT steps.
You need to first plan wjat needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can given an OUTPUT.
yu can also call a tool if required from the list of the tools.
for every tooll cll wait for the observe step which is the output from the  called tool

Rules:
- Strictly Follow the given JSON output format
- Only run one step at the time 
The sequence of step is start (where user gives an input) ,Plan(That can multiple times)

Output JSON format:
{"step":"start |"PLAN"|"OUTPUT"|"TOOL,"Content":String "tool":"string" , "input":"string"}

Available Tools
 get_weather(city):Takes the city name as an input string and returns 
 the weather info about the city.
 Example 1:
 START : what is the weather of Delhi
 PLAN:{"step":"PLAN":"content":"Seems like,user is interested in getting weather of Delhi in India"}
 PLAN:{"step":"PLAN":"content":"Lets see if we have any available tool from the list of available tools"}
 PLAN:{"step":"PLAN":"content":"Greate, we have get_weather tool available for this query"}
 PLAN:{"step":"PLAN":"content":"I need to call get_weather tool for delhi as the input"}
 PLAN:{"step":"PLAN": "Tool":"get_weather" input":"delhi"}
 PLAN:{"step":"PLAN": "OBSERVE":"tool" "content":"The temp in delhi is cold with 10 c"}
 PLAN:{"step":"PLAN":"content":"I got the weather info about delhi"}
 OUTPUT:{"step":"OUTPUT":"content":"The current weather in delhi is 10 c"}

   

"""

class MMyOutFormat(BaseModel):
    step:str = Field(...,description="The Id of the step. Example: PLAN,OUTPUT,TOOL,etc")
    content: Optional[str]=Field(None,description="The optional string content for the step")
    tool:Optional[str]=Field(None,description="The ID of the tool to call")
    input:Optional[str]=Field(None,description="The input params for the tool")

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if response.status_code == 200:
        print(f"The weather in {city} is {response.text}")

    if response.status_code == 400:
        print(f"Something went wrong")


available_tools={
    "get_weather":get_weather
}

def main():

    message_history=[
        {"role" : "system" , "content" : SYSTEM_PROMPT}
    ]
    while True:
        user_query=input("Ask anything!!!")
        message_history.append({"role" :"user" ,"content":user_query})

        while True:
            response=client.chat.completions.parse(
                model="gpt-4o-mini",
                response_format=MMyOutFormat,
                messages=message_history
            )

            raw=response.choices[0].message.content
            message_history.append({"role":"assistant","content":raw})

            parsed_result=response.choices[0].message.parsed
           
            if parsed_result.step == 'START':
                print("🔥" ,parsed_result.content)
                continue
            if parsed_result.step == "TOOL":
                tool_to_call=parsed_result.tool
                tool_input=parsed_result.input
                print(f"🛠:{tool_to_call}( {tool_input})")

                tool_response=available_tools[tool_to_call](tool_input)
                print(f"{tool_to_call} ( {tool_input}) =  {tool_response}")
                message_history.append({"role":"assistant" ,"content":json.dumps(
                    {"step":"OBSERVE" ,"tool":tool_to_call,"input":tool_input,"output":tool_response}
                )})
                continue
            if parsed_result.step == 'PLAN':
                print(f"🧠", parsed_result.content)
                continue
            if parsed_result.step == 'OUTPUT':
                print(parsed_result.content)
                break

main()


  



