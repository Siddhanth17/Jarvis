import speech_recognition as sr 
import threading 
from Automation.Brain import auto_brain

def listen_and_process():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                text = r.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                if text:
                    auto_brain(text)
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

def jarvis():
    t1 = threading.Thread(target=listen_and_process)
    t1.start()
    t1.join()

if __name__ == "__main__":
    jarvis()