# File name: dataset-thread.py
# Platform: Python 3.8.8 on Ubuntu Linux 18.04
# Required Package(s): mediapipe, pynput
# Date: 2021.05.18
# Name: Dohun Kim, DaeHeon Yoon


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

TIMEOUT = 1 / 30

def process_hand_asdf(data):

    with open('log.csv', 'a') as log:
        log.write()


def hand_thread():

    # mediapipe hands module
    mp_hands   = mp.solutions.hands

    # webcam input
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        old_timestamp = time.time()

        while cap.isOpened():
            if (time.time() - old_timestamp) <= TIMEOUT:
                continue

            old_timestamp = time.time()

            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                continue
                
            image.flags.writable = False
            results = hands.process(image)

            '''
            ADD HERE: 
                func() results -> log.csv
            '''

            process_hand_asdf(results)





####################################### main ######################################

if __name__ == '__main__':

    open('log.csv', 'w').close()  # delete before log
    
    key  = threading.Thread(target=keyboard_thread)
    hand = threading.Thread(target=hand_thread)

    key.start()
    hand.start()
