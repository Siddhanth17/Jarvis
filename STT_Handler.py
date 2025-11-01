import speech_recognition as sr
import time
import sys

# Initialize the recognizer once
r = sr.Recognizer()

def listen() -> str | None:
    """
    Listens for speech from the microphone and returns the recognized text
    using Google's Web Speech API.
    """
    with sr.Microphone() as source:
        # Adjust for ambient noise for better accuracy
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("[STT] Say something!")

        try:
            # Listen for audio
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"[STT] An error occurred during audio capture: {e}", file=sys.stderr)
            return None

    # Recognize speech
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"[STT] Could not request results from Google Speech Recognition service; {e}", file=sys.stderr)
        time.sleep(1)
        return None
    except Exception as e:
        print(f"[STT] An unexpected error occurred during recognition: {e}", file=sys.stderr)
        return None