import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

def main():
    r=sr.Recognizer() #speech to text
    
    with sr.Microphone() as source:  #Mic Access
        r.adjust_for_ambient_noise(source) #disable noise fromthe background 
        r.pause_threshold=2 #if user takes a pause than recogo with start afetr 2 sec
        
        print("Speak something")
        audio=r.listen(source) #Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
        
        print("Processing Audio... (STT)")
        stt=r.recognize_google(audio) #provider is google fromthat we are recogo text
        
        #printing that text
        print("You said:",stt)
        
        SYSTEM_PROMPT="""
            you are an expert voice agent whose name 
            is gaurav alexa. you are given an the transcript
            of what  user has said using voice.
            You neeed to generate the output as if you are an voice 
            agent and whatever you speak will be converted back into the 
            audio using AI and played back to user.
            
        """
        
        
        response=client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":stt}
                
            ]
        )
        
        print("AI Response", response.choices[0].message.content)
        
        
main()
        
        
        