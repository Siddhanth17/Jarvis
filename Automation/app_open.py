import pyautogui as gui
import subprocess
import time

def open_app(text):
    try:
        subprocess.run(text)
    except Exception as e:
        gui.press('win')
        time.sleep(0.2)
        gui.write(text)
        time.sleep(0.2)
        gui.press('enter')

while True:
    app_name = input("Enter the application name to open (or 'exit' to quit): ")
    if app_name.lower() == 'exit':
        break
    open_app(app_name)  