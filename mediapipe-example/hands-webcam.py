'''
Original demo code can be found at:
  https://google.github.io/mediapipe/solutions/hands.html
'''

import cv2
import mediapipe as mp

import sys, os

sys.path.append(os.pardir)


from utils import live_plotter
import numpy as np

import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.random.randn(len(x_vec))
line1 = []

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    if results.multi_hand_landmarks:
      val = results.multi_hand_landmarks[0].landmark[8].z
      y_vec[-1] = val
      line1 = live_plotter(x_vec, y_vec, line1)
      y_vec = np.append(y_vec[1:], 0.0)

    


      # time.sleep(0.3)
    #
    # else:
    #   print(0)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
