import asyncio
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client=OpenAI()
async_client=AsyncOpenAI()

async def tts(speech:str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speeks in cheerful manner with full of delight and happy",
        input=speech,
        response_format="pcm",
        
    )as response :
        await LocalAudioPlayer().play(response)
    

def main():
    r=sr.Recognizer() #speech to text
    
    with sr.Microphone() as source:  #Mic Access
        r.adjust_for_ambient_noise(source) #disable noise fromthe background 
        r.pause_threshold=2 #if user takes a pause than recogo with start afetr 2 sec
        
        SYSTEM_PROMPT="""
                you are an expert voice agent whose name 
                is gaurav alexa. you are given an the transcript
                of what  user has said using voice.
                You neeed to generate the output as if you are an voice 
                agent and whatever you speak will be converted back into the 
                audio using AI and played back to user.
                
            """
        
        messages=[
              {"role":"system","content":SYSTEM_PROMPT},
        ]
        
        while True:
        
            print("Speak something")
            audio=r.listen(source) #Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
            
            print("Processing Audio... (STT)")
            stt=r.recognize_google(audio) #provider is google fromthat we are recogo text
            
            #printing that text
            print("You said:",stt)
            
            
            messages.append( {"role":"user","content":stt})
            
            response=client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            
            print("AI Response", response.choices[0].message.content)
            asyncio.run(tts(speech= response.choices[0].message.content))
        
        
main()
        
        
        