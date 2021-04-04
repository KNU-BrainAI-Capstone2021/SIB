'''
Original demo code can be found at:
  https://google.github.io/mediapipe/solutions/hands.html

copy of hands-webcom-dataset.py
'''

import cv2
import mediapipe as mp
import time


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with open('log.txt', 'w') as log:
    print("new log file")

start_time = time.time()

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

    time.sleep(0.3)

    with open('log.txt', 'a') as log:
        log.write('{:f},'.format(time.time() - start_time))
        if results.multi_hand_landmarks:
            if len(results.multi_handedness) == 1:
                if results.multi_handedness[0].classification[0].label == 'Left':
                    for landmark in results.multi_hand_landmarks[0].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
                    for i in range(22):
                        log.write(",")
                else:  # Right
                    for i in range(22):
                        log.write(",")
                    for landmark in results.multi_hand_landmarks[0].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
            else: # two hands
                if results.multi_handedness[0].classification[0].label == 'Left':
                    for landmark in results.multi_hand_landmarks[0].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
                    for landmark in results.multi_hand_landmarks[1].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
                else: # Right
                    for landmark in results.multi_hand_landmarks[1].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
                    for landmark in results.multi_hand_landmarks[0].landmark:
                        log.write('{:f},{:f},{:f},'.format(landmark.x, landmark.y, landmark.z))
                    log.write('{:f},'.format(results.multi_handedness[0].classification[0].score))
        else:
            for i in range(44):
                log.write(",")
        log.write("\n")


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
