import requests
from playsound import playsound
import os 
from typing import Union 

def generate_audio(text:str,voices :str="Brian"):
    url : str = f"https://api.streamelements.com/kappa/v2/speech?voice={voices}&text={{{text}}}"
    headers = {'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/605.1.15(KHTML,likeGecko)Chrome/119.0.0.0 Safari/605.1.15'}

    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except Exception as e:
        print("Error in generate_audio function:",e)
        return None

def speak(text: str,voices: str = "Brian", folder: str="", extension: str = ".mp3") -> Union[None,str]:
    try:
        result_content = generate_audio(text,voices)
        file_path = os.path.join(folder,f"{voices}{extension}")
        with open(file_path,"wb")as f:
            f.write(result_content)
        playsound(file_path,)
        os.remove(file_path)
        return None
    except Exception as e:
        print("Error in speak function:",e)
        return None
speak("Hello, this is a test message")