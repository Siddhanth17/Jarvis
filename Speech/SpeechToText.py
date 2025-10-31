import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_loop():
    """Shows running status message in background."""
    while True:
        print(Fore.GREEN + "🎙️ Speech-to-Text is running... Press Ctrl+C to stop.", end="\r", flush=True)

def translate_text(text):
    """Translate any detected text to English."""
    try:
        english_text = translate(text, 'en', 'auto')
        return english_text
    except Exception as e:
        return f"[Translation Error: {e}]"

def speech_to_text():
    """Continuously listens to speech and prints recognized + translated text."""
    recognizer = sr.Recognizer()

    # 🔧 Corrected and tuned parameters
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300  # Lower threshold to detect normal voice
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    try:
        with sr.Microphone() as source:
            print(Fore.CYAN + "Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(Fore.GREEN + "Ready! Speak something...")

            while True:
                try:
                    print(Fore.LIGHTYELLOW_EX + "\nListening...")
                    audio = recognizer.listen(source, timeout=None)
                    print(Fore.YELLOW + "Processing audio...")

                    # Recognize the speech
                    recognized_text = recognizer.recognize_google(audio, language="en-IN").lower()
                    if recognized_text:
                        translated_text = translate_text(recognized_text)
                        print(
                            Fore.CYAN + "You said: " + 
                            Fore.WHITE + f"{recognized_text}" +
                            Fore.MAGENTA + f" | Translated: {translated_text}"
                        )
                    else:
                        print(Fore.RED + "No speech detected. Try again.")

                except sr.UnknownValueError:
                    print(Fore.RED + "Sorry, I couldn’t understand that.")
                except sr.RequestError as e:
                    print(Fore.RED + f"API Error: {e}")
                except KeyboardInterrupt:
                    print(Fore.RED + "\nStopped by user.")
                    break
    except Exception as e:
        print(Fore.RED + f"Microphone error: {e}")

def main():
    """Runs the program with two threads: one for listening, one for status display."""
    stt_thread = threading.Thread(target=speech_to_text, name="STTThread")
    print_thread = threading.Thread(target=print_loop, name="PrintThread", daemon=True)

    stt_thread.start()
    print_thread.start()

    # Keep the main program alive until speech thread stops
    stt_thread.join()

if __name__ == "__main__":
    main()
