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
    try:
        num = key2num(key)
    except:
        return

    if num == None:
        return

    curr_pressed[num] = 1

    print(curr_pressed)


def on_release(key):
    try:
        num = key2num(key)
    except:
        return

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

def process_hand_asdf(hand_data):
    with open('log.csv', 'a') as log:
        if hand_data.multi_hand_landmarks:
            for landmark in hand_data.multi_hand_landmarks[0].landmark:
                log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
        else:
            for i in range(22):
                log.write(",")
        
        for key in curr_pressed[:-1]:
            log.write('{:d},'.format(key))
        log.write('{:d}'.format(curr_pressed[-1]))
        
        log.write('\n')


def hand_thread(flip=False, show_cam=False):

    # mediapipe hands module
    mp_drawing = mp.solutions.drawing_utils
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
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if flip:
                image = cv2.flip(image, 1)
                
            image.flags.writeable = False
            hand_data = hands.process(image)

            process_hand_asdf(hand_data)
            
            if show_cam:
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                if hand_data.multi_hand_landmarks:
                    for hand_landmarks in hand_data.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
            




####################################### main ######################################

if __name__ == '__main__':

    open('log.csv', 'w').close()  # delete before log
    
    key  = threading.Thread(target=keyboard_thread)
    hand = threading.Thread(target=hand_thread, kwargs={'show_cam': True})

    key.start()
    hand.start()
