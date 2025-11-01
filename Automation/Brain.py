from .app_open import open_app
from .website_open import open_website
from .web_data import websites
import pyautogui as gui
from time import sleep
from .music import play_music_on_youtube
from .spotify import open_spotify_playlist

class TTS_Mock:
    def speak(self, text):
        print(f"TTS: {text}")
fast_tts_bf = TTS_Mock()

def close():
    gui.hotkey('alt','f4')

def open_brain(text):
    name_to_open = text.strip().lower()
    
    if name_to_open in websites:
        fast_tts_bf.speak(f"Opening website {name_to_open}")
        open_website(name_to_open, is_single_key=True)
    else:
        fast_tts_bf.speak(f"Opening application {name_to_open}")
        open_app(name_to_open)

 
def auto_brain(text):
    text = text.lower().strip()
    
    if text.startswith("open"):
        name_to_open = text[len("open "):].strip()
        if name_to_open:
             open_brain(name_to_open)
        else:
             fast_tts_bf.speak("Please tell me what you want to open.")
             
    elif "close" in text or "exit" in text or "quit" in text:
        close()
        
    elif "play music" in text or "play song" in text:
        fast_tts_bf.speak("Which song do you want to play?")
        x = input("Enter song name: ") 
        play_music_on_youtube(x)
        
    elif "play on spotify" in text or "open on spotify" in text:
        fast_tts_bf.speak("Which song do you want to play on spotify?")
        y = input("Enter song name: ")
        open_spotify_playlist(y)
        
    else:
        fast_tts_bf.speak("Sorry, I didn't understand that command.")