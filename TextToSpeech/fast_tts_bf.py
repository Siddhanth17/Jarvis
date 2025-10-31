import os
import subprocess
import tempfile
import threading
import sys
from playsound import playsound

DEFAULT_VOICE = "en-US-AriaNeural"

def _play_and_cleanup(path: str):
    try:
        playsound(path)
    except Exception as e:
        print("Playback error:", e)
    finally:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

def speak(text: str, voice: str = DEFAULT_VOICE) -> None:
    try:
        # create temp file and get its name from the NamedTemporaryFile object
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            output_file = tmp.name

        # build command list for edge-tts CLI (avoids shell quoting issues)
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", output_file
        ]
        # generate TTS file
        subprocess.run(cmd, check=True)

        # play in background and remove file when done
        t = threading.Thread(target=_play_and_cleanup, args=(output_file,), daemon=True)
        t.start()
    except FileNotFoundError:
        print("edge-tts executable not found. Install it or ensure it's on PATH.")
    except Exception as e:
        print("Error in fast_tts_bf speak function:", e)

while True:
    x = input()
    speak(x)