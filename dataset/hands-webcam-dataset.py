'''
Original demo code can be found at:
  https://google.github.io/mediapipe/solutions/hands.html
'''

import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

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

    # print(results.multi_hand_landmarks)

    a = results.multi_hand_landmarks[0]
    b = a.landmark[0]
    print(type(b.x))


    c = results.multi_handedness

    for i, multi_handedness in enumerate(results.multi_handedness):
      tmp = multi_handedness.classification
      for j, x in enumerate(tmp):
        print(i, j, x.label)


    # d = c[0].classification

    # print(d[0].label)

    # print(results.multi_hand_landmarks[0])
    break


    results.multi_hand_landmarks[0].landmark[0].x

    results.multi_handness[0].classification[0].label

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
