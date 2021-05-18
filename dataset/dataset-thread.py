# File name: dataset-thread.py
# Platform: Python 3.8.8 on Ubuntu Linux 18.04
# Required Package(s): mediapipe, pynput
# Date: 2021.05.18
# Name: Dohun Kim


################################# import packages #################################

import threading
import time

from pynput import keyboard

import cv2
import mediapipe as mp



############################# keyboard input - pynput #############################

mapping_dict = {'a': 0, 's': 1, 'd': 2, 'f': 3}

curr_pressed = [0] * len(mapping_dict)


def flush_input():
    import sys, termios
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def key2num(key):
    if key.char in mapping_dict.keys():
        return mapping_dict[key.char]
    
    return None


def on_press(key): 
    num = key2num(key)

    if num == None:
        return False 

    curr_pressed[num] = 1

    print(curr_pressed)


def on_release(key):
    num = key2num(key)

    if num == None:
        return

    curr_pressed[num] = 0

    print(curr_pressed)


def keyboard_thread():
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:

        listener.join()
        
        flush_input()
        print('\nkeyboard thread terminated')



############################ hand landmark - mediapipe ############################

def hand_thread():
    while True:
        print('hello')
        time.sleep(1)



####################################### main ######################################

if __name__ == '__main__':
    key  = threading.Thread(target=keyboard_thread)
    hand = threading.Thread(target=hand_thread)

    key.start()
    hand.start()
