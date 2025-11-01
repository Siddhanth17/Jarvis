import webbrowser
import pyautogui as gui
import time

def open_spotify_playlist(song_name):
    webbrowser.open(f"https://open.spotify.com/search/{song_name}")
    gui.hotkey('ctrl','shift', 'l')
    time.sleep(2)
    gui.write(song_name)
    gui.rightClick(790,500)

open_spotify_playlist("phele nazar")