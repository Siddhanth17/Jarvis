from TextToSpeech import fast_tts_bf
from NetHyTech_STT import listen 
import threading

def check():
    output_text = "" 
    while True:
        try:
            with open("output.txt", "r") as f:
                output_text = f.read().strip()  
                if input_text != output_text:
                    input_text = output_text
                    if output_text:
                        print(f"New input detected: {output_text}")
                        fast_tts_bf.speak(output_text)
        except FileNotFoundError:
            pass

t1 = threading.Thread(target=listen, daemon=True)
t2 = threading.Thread(target=check, daemon=True)
t1.start()
t2.start()
t1.join()
t2.join()    
