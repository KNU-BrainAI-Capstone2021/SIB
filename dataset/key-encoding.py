from pynput import keyboard

import sys, os 
sys.path.append(os.pardir)

from utils import flush_input


mapping_dict = {'a': 0, 's': 1, 'd': 2, 'f': 3}

curr_pressed = [0] * len(mapping_dict)


def key2num(key):
    assert key.char in mapping_dict.keys()
    return mapping_dict[key.char]


def on_press(key): 
    if key == keyboard.Key.esc:
        flush_input()
        return False 

    num = key2num(key)
    curr_pressed[num] = 1

    print(curr_pressed)


def on_release(key):
    num = key2num(key)
    curr_pressed[num] = 0

    print(curr_pressed)


with keyboard.Listener( 
    on_press=on_press, 
    on_release=on_release) as listener: 

    listener.join()
