# File name: dataset-thread.py
# Platform: Python 3.8.8 on Ubuntu Linux 18.04
# Required Package(s): mediapipe, pynput
# Date: 2021.06.19
# Name: Dohun Kim, DaeHeon Yoon


################################# import packages #################################

import time
from threading import Thread
from queue import Queue

import numpy as np
from tensorflow.keras.models import load_model

import cv2
import mediapipe as mp

q = Queue()


########################### key prediction - tensorflow ###########################

def model_thread(model_path):

    # load pretrained tensorflow model
    model = load_model(model_path)

    model.summary()
    
    while True:
        if not q.empty():
            hand_np = q.get()
            pred = model.predict(hand_np)
            print(np.argmax(pred))



############################ hand landmark - mediapipe ############################

FPS     = 30
TIMEOUT = 1 / FPS


def hand_to_numpy(hand_data):
    if hand_data.multi_hand_landmarks:
        result = []
        for landmark in hand_data.multi_hand_landmarks[0].landmark:
            result += [landmark.x, landmark.y, landmark.z]
        return np.array([result])
    return None


def hand_thread(flip=False):

    # mediapipe hands module
    mp_hands = mp.solutions.hands

    # webcam input
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        old_timestamp = time.time()

        while cap.isOpened():
            # while-loop with fixed frame rate(FPS)
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

            hand_np = hand_to_numpy(hand_data)

            if hand_np is not None:
                q.put(hand_np)



####################################### main ######################################

if __name__ == '__main__':

    model_path = 'saved_model/model_mlp_space.h5'
    
    key  = Thread(target=model_thread, args=(model_path,))
    hand = Thread(target=hand_thread)

    key.start()
    hand.start()
