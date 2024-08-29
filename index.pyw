import json
import keyboard
import subprocess
import threading
import time
import os

with open('app.aa', 'w', encoding='utf-8') as file:
    file.write('start')

pressed_keys = set()

def clear_pressed_keys():
    global pressed_keys
    while True:
        time.sleep(2)
        pressed_keys = set()

def check_unix_json(keyboard_event):
    global pressed_keys
    if keyboard_event.event_type == keyboard.KEY_DOWN:
        key = keyboard_event.name.lower()
        pressed_keys.add(key)
        with open('unix.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for combination, file_path in data.items():
                keys = combination.split(' + ')
                if set(keys) == pressed_keys:
                    subprocess.Popen(['start', '', file_path], shell=True)
                    pressed_keys = set()

def monitor_file():
    while True:
        time.sleep(1)
        if not os.path.exists('app.aa'):
            print("Файл 'app.aa' не знайдено. Завершення програми.")
            os._exit(0) 

file_monitor_thread = threading.Thread(target=monitor_file)
file_monitor_thread.daemon = True
file_monitor_thread.start()

keyboard.hook(check_unix_json)

clear_keys_thread = threading.Thread(target=clear_pressed_keys)
clear_keys_thread.daemon = True
clear_keys_thread.start()

keyboard.wait()