import asyncio
import subprocess
import sys

def install_requirements():
    required_packages = ['SpeechRecognition', 'pyaudio']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

from Speech.speech_handler import listen

def main():
    while True:
        text = listen()
        if text:
            print(f"You said: {text}")

if __name__ == "__main__":
    main()