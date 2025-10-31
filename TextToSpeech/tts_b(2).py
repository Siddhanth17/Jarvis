import requests
import playsound
import os 
from typing import Union 

def generate_audio(text:str,voices :str="Brian"):
    url : str = f"https://api.streamelements.com/kappa/v2/speech?voice={voices}&text={{{text}}}"
    headers = {'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/605.1.15(KHTML,likeGecko)Chrome/119.0.0.0 Safari/605.1.15'}

    try:
        result = requests.get(url,headers=headers)
        return result.content
    except Exception as e:
        print("Error in generate_audio function:",e)
        return None

def speak(text:str,voices :str="Brian")->None:
    try:
        audio_data = generate_audio(text,voices)
        if audio_data is None:
            print("Failed to generate audio.")
            return
        
        temp_file = "temp_speech.mp3"
        with open(temp_file,"wb") as f:
            f.write(audio_data)
        
        playsound.playsound(temp_file)
        os.remove(temp_file)
    except Exception as e:
        print("Error in speak function:",e)

if __name__ == "__main__":
    speak("Hello, this is a test message")