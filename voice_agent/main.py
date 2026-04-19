import speech_recognition as sr

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
        
        
main()
        
        
        