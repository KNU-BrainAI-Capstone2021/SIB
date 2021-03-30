
import cv2
import mediapipe as mp

import time

import sys, os 
sys.path.append(os.pardir)

from utils import file_append, periodic_task, get_now



hands = mp.solutions.hands.Hands(min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

file_path = './mediapipe_output.log'


@periodic_task(1)
def hello(): 
    print(get_now())

    if cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            return

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        output_str = '%s\n%s\n%s\n' %(get_now(),
                                      results.multi_handedness,
                                      results.multi_hand_landmarks)
        
        file_append(file_path, output_str)
        



        # # Draw the hand annotations on the image.
        # image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         mp_drawing.draw_landmarks(image, 
        #                                 hand_landmarks, 
        #                                 mp_hands.HAND_CONNECTIONS)
        #         cv2.imshow('MediaPipe Hands', image)
        #         if cv2.waitKey(5) & 0xFF == 27:
        #             break


hello()


# time.sleep(threading.TIMEOUT_MAX)
time.sleep(10)

cap.release()