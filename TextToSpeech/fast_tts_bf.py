import os
import subprocess
import tempfile
import threading
import sys
import shlex

try:
    from playsound import playsound as _playsound
except Exception:
    _playsound = None

# optional pyttsx3 fallback
try:
    import pyttsx3
except Exception:
    pyttsx3 = None

DEFAULT_VOICE = "en-CA-LiamNeural"

def _play_file(path: str):
    try:
        if _playsound:
            _playsound(path)
            return
    except Exception:
        pass

    # platform fallbacks
    try:
        if sys.platform.startswith("win"):
            # use start / wait via powershell to play file
            subprocess.run(["powershell", "-Command", f'Start-Process -FilePath "{path}" -Verb open'], check=False)
        elif sys.platform == "darwin":
            subprocess.run(["afplay", path], check=False)
        else:
            # linux: try mpg123, ffplay, or xdg-open
            for cmd in (["mpg123", path], ["ffplay", "-nodisp", "-autoexit", path], ["xdg-open", path]):
                try:
                    subprocess.run(cmd, check=False)
                    break
                except Exception:
                    continue
    except Exception as e:
        print(f"[TTS] Playback fallback error: {e}", file=sys.stderr)

def _play_and_cleanup(path: str):
    try:
        _play_file(path)
    finally:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

def _speak_with_pyttsx3(text: str):
    try:
        if pyttsx3:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            return True
    except Exception as e:
        print(f"[TTS] pyttsx3 error: {e}", file=sys.stderr)
    # Windows PowerShell fallback
    if sys.platform.startswith("win"):
        try:
            # Use PowerShell to speak using System.Speech
            safe = text.replace('"', '`"')
            ps = f'Add-Type –AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{safe}")'
            subprocess.run(["powershell", "-Command", ps], check=False)
            return True
        except Exception as e:
            print(f"[TTS] PowerShell TTS error: {e}", file=sys.stderr)
    return False

def speak(text: str, voices: str = DEFAULT_VOICE) -> None:
    """
    Try edge-tts CLI -> play mp3. If that fails, fallback to pyttsx3 or platform TTS.
    This function returns quickly; audio playback runs in background threads.
    """
    if not text or not str(text).strip():
        return

    text = str(text).strip()

    # Try edge-tts CLI first
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name

        cmd = ["edge-tts", "--text", text, "--voice", voices, "--write-media", tmp_path]
        try:
            subprocess.run(cmd, check=True)
            # play in background and remove file when done
            threading.Thread(target=_play_and_cleanup, args=(tmp_path,), daemon=True).start()
            return
        except FileNotFoundError:
            # edge-tts not installed
            pass
        except subprocess.CalledProcessError as cpe:
            # edge-tts failed (invalid voice or other). cleanup and fall back
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
        except Exception:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
    except Exception as e:
        # could not create temp file or something else; continue to fallback
        print(f"[TTS] edge-tts attempt error: {e}", file=sys.stderr)

    # Fallback to pyttsx3 or platform TTS
    try:
        ok = _speak_with_pyttsx3(text)
        if ok:
            return
    except Exception as e:
        print(f"[TTS] fallback pyttsx3 error: {e}", file=sys.stderr)

    # Final fallback: attempt to play using platform TTS commands or notify
    print("[TTS] No TTS backend succeeded. Install 'edge-tts' (CLI) or 'pyttsx3' for fallback.", file=sys.stderr)