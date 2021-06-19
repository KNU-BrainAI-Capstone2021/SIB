# File name: dataset-thread.py
# Platform: Python 3.8.8 on Ubuntu Linux 18.04
# Required Package(s): mediapipe, pynput
# Date: 2021.06.19
# Name: Dohun Kim, DaeHeon Yoon


################################# import packages #################################

import threading
import time

import tensorflow as tf

import cv2
import mediapipe as mp


########################### key prediction - tensorflow ###########################

def model_thread(model_path):

    # load pretrained tensorflow model
    model = tf.keras.models.load_model(model_path)

    model.summary()
    
    while True:
        time.sleep(1)
        pass


############################ hand landmark - mediapipe ############################

FPS     = 30
TIMEOUT = 1 / FPS

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

            # ADD HERE: hand_data to numpy input



####################################### main ######################################

if __name__ == '__main__':

    open('log.csv', 'w').close()  # delete before log

    model_path = 'saved_model/model_mlp_space.h5'
    
    key  = threading.Thread(target=model_thread, kwargs={'model_path': model_path})
    hand = threading.Thread(target=hand_thread, kwargs={'show_cam': True})

    key.start()
    hand.start()
