from pynput import keyboard 

import sys, os 
sys.path.append(os.pardir)

from utils import flush_input, file_append, get_now


current_pressed = set()
file_path = './key.log'

def on_press(key): 
    if key == keyboard.Key.esc:
        flush_input()
        return False 

    current_pressed.add(key)

    str = f'{get_now()} {current_pressed} pressed\n'
    file_append(file_path, str)
    
def on_release(key):     
    str = f'{get_now()} {key} released\n'
    file_append(file_path, str)

    if key in current_pressed: 
        current_pressed.remove(key) 
        
with keyboard.Listener( 
    on_press=on_press, 
    on_release=on_release) as listener: 
    listener.join()
