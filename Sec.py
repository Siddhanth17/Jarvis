from TextToSpeech import fast_tts_bf

# --- STT IMPORT: Tries to use the STT_Handler we created ---
try:
    # We now import the 'listen' function from our new STT_Handler.py
    from STT_Handler import listen
except Exception as _e:
    listen = None
    print(f"[Sec] Warning: could not import listen from STT_Handler: {_e}")
# -----------------------------------------------------------

import threading
import time
import os
import sys
import inspect
import asyncio

def write_output(text: str):
    """Writes the recognized text to output.txt."""
    try:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"[Sec] Error writing output.txt: {e}", file=sys.stderr)

def _import_fallback_listen():
    """Try common fallback listen implementations and return callable or None."""
    candidates = [
        "Speech.speech_handler",
        "Speech.SpeechToText",
        "speech_handler",
    ]
    for cand in candidates:
        try:
            mod = __import__(cand, fromlist=["listen"])
            if hasattr(mod, "listen") and callable(mod.listen):
                print(f"[Sec] Fallback listen found in '{cand}'")
                return mod.listen
        except Exception:
            continue
    return None

def _call_listen_callable(fn):
    """Call a listen callable (sync or coroutine) and return its result or None."""
    try:
        if inspect.iscoroutinefunction(fn):
            return asyncio.run(fn())
        result = fn()
        if asyncio.iscoroutine(result):
            return asyncio.run(result)
        return result
    except Exception as e:
        print(f"[Sec] Exception while calling listen: {e}", file=sys.stderr)
        return None

def speech_listener():
    """Continuously call the STT listen() and write recognized text to output.txt.
       Also speak immediately when new speech is recognized."""

    print("[Sec] speech_listener started")

    last_seen = ""

    local_listen = listen
    if not callable(local_listen):
        print("[Sec] Primary listen() not available; attempting fallback...")
        local_listen = _import_fallback_listen()
        if not callable(local_listen):
            print("[Sec] No usable listen() found. Exiting speech_listener.")
            return
    
    # 💡 DIAGNOSTIC PRINT 💡
    print(f"[Sec] Listen function successfully initialized: {local_listen}")

    while True:
        try:
            # call the listen callable and get text
            text = _call_listen_callable(local_listen)

            if not text:
                # nothing returned; short sleep and retry
                time.sleep(0.2)
                continue

            text = str(text).strip()

            if text and text != last_seen:
                last_seen = text

                print(f"[Sec] Recognized: {text!r}")

                write_output(text)

                # **Speak immediately in background to avoid blocking listener**
                # This is the line that makes the program speak the recognized words
                try:
                    threading.Thread(target=fast_tts_bf.speak, args=(text,), daemon=True).start()
                except Exception as e:
                    print(f"[Sec] Error starting TTS thread: {e}", file=sys.stderr)
            
            elif text == last_seen:
                # Text matched last_seen, skip speak/write
                pass

        except Exception as e:
            print(f"[Sec] Error in speech_listener loop: {e}", file=sys.stderr)
            time.sleep(0.5)

def check():
    """Watch output.txt for changes and speak new text via fast_tts_bf.speak (background)."""

    print("[Sec] check started")

    last_text = ""
    # Ensure output.txt exists
    if not os.path.exists("output.txt"):
        open("output.txt", "w", encoding="utf-8").close()

    while True:
        try:
            with open("output.txt", "r", encoding="utf-8") as f:
                current_text = f.read().strip()
            if current_text and current_text != last_text:
                last_text = current_text
                print(f"[Sec] New input detected (file): {current_text!r}")
                try:
                    # Speak new text written to the file
                    threading.Thread(target=fast_tts_bf.speak, args=(current_text,), daemon=True).start()
                except Exception as e:
                    print(f"[Sec] Error starting speak thread from check: {e}", file=sys.stderr)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[Sec] Error in check loop: {e}", file=sys.stderr)
        time.sleep(0.2)

if __name__ == "__main__":
    # start listener and checker threads
    t_listener = threading.Thread(target=speech_listener, name="SpeechListener", daemon=True)
    t_checker = threading.Thread(target=check, name="Checker", daemon=True)
    t_listener.start()
    t_checker.start()

    try:
        # keep main alive
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[Sec] Stopped by user.")