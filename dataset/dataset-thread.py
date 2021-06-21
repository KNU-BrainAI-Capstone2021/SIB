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

flag_stop = False


############################# keyboard input - pynput #############################

mapping_dict = {'a': 0, 's': 1, 'd': 2, 'f': 3}

curr_num = None
curr_vector = [0] * len(mapping_dict)


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
        return False

    if num == None:
        return False
    
    global curr_num
    if curr_num != None:
        curr_vector[curr_num] = 0
    curr_vector[num] = 1
    curr_num = num

    # print(curr_vector)


def on_release(key):
    try:
        num = key2num(key)
    except:
        return False

    if num == None:
        return False
    
    global curr_num
    if curr_num == num:
        curr_vector[num] = 0
        curr_num == None

    # print(curr_vector)


def keyboard_thread():
    global flag_stop

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:

        listener.join()
        
    flag_stop = True
    flush_input()
    print('keyboard_thread() terminated.')



############################ hand landmark - mediapipe ############################

FPS     = 30
TIMEOUT = 1 / FPS

def process_hand_asdf(hand_data):
    with open('log.csv', 'a') as log:
        if hand_data.multi_hand_landmarks:
            for landmark in hand_data.multi_hand_landmarks[0].landmark:
                log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
        else:
            for i in range(21):
                log.write(",,,")
        
        for key in curr_vector[:-1]:
            log.write('{:d},'.format(key))
        log.write('{:d}'.format(curr_vector[-1]))
        
        log.write('\n')


def hand_thread(flip=False, show_cam=False):

    # mediapipe hands shortcuts
    mp_drawing = mp.solutions.drawing_utils
    mp_hands   = mp.solutions.hands

    # webcam input
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('cv2.VideoCapture open failed.')
        return
    
    # create mediapipe hands module
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        # while-loop with fixed frame rate(FPS)
        old_timestamp = time.time()
        while not flag_stop:
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
                
                # add hand landmarks to image
                if hand_data.multi_hand_landmarks:
                    for hand_landmarks in hand_data.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, 
                                                  mp_hands.HAND_CONNECTIONS)

                # add current pressed key to image
                org       = (50, 50)
                fontFace  = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color     = (0, 0, 255) # (B, G, R)
                thickness = 2

                image = cv2.putText(image, str(curr_vector), org, fontFace, 
                                    fontScale, color, thickness, cv2.LINE_AA)

                # show image
                cv2.imshow('MediaPipe Hands', image)
                
                if cv2.waitKey(5) & 0xFF == 27:
                    break
    
    cap.release()
    print('hand_thread() terminated.')



####################################### main ######################################

if __name__ == '__main__':

    open('log.csv', 'w').close()  # delete before log
    
    key  = threading.Thread(target=keyboard_thread)
    hand = threading.Thread(target=hand_thread, kwargs={'show_cam': True})

    key.start()
    hand.start()

    key.join()
    hand.join()
