import cv2 as cv
import numpy as np
import mediapipe as mp

print(mp.solutions.hands)

print(mp)

print(mp.__file__)

# Webcam
camera = cv.VideoCapture(0)

# Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Canvas
canvas = np.zeros((480,640,3), dtype=np.uint8)

# Previous point
prev_x = 0
prev_y = 0

# Default color
draw_color = (255,0,0)

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv.flip(frame,1)
    frame = cv.resize(frame,(640,480))

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # -----------------------------------
    # COLOR BUTTONS
    # -----------------------------------

    cv.rectangle(frame,(0,0),(100,65),(255,0,0),-1)
    cv.putText(frame,"Blue",(15,40),
               cv.FONT_HERSHEY_SIMPLEX,
               0.7,(255,255,255),2)

    cv.rectangle(frame,(100,0),(200,65),(0,255,0),-1)
    cv.putText(frame,"Green",(110,40),
               cv.FONT_HERSHEY_SIMPLEX,
               0.7,(255,255,255),2)

    cv.rectangle(frame,(200,0),(300,65),(0,0,255),-1)
    cv.putText(frame,"Red",(225,40),
               cv.FONT_HERSHEY_SIMPLEX,
               0.7,(255,255,255),2)

    cv.rectangle(frame,(300,0),(400,65),(0,255,255),-1)
    cv.putText(frame,"Yellow",(305,40),
               cv.FONT_HERSHEY_SIMPLEX,
               0.6,(0,0,0),2)

    cv.rectangle(frame,(500,0),(640,65),(50,50,50),-1)
    cv.putText(frame,"Clear",(530,40),
               cv.FONT_HERSHEY_SIMPLEX,
               0.7,(255,255,255),2)

    # -----------------------------------
    # HAND DETECTION
    # -----------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Index finger tip
            index_finger = hand_landmarks.landmark[8]

            h, w, c = frame.shape

            center_x = int(index_finger.x * w)
            center_y = int(index_finger.y * h)

            cv.circle(frame,
                      (center_x, center_y),
                      10,
                      (255,255,255),
                      -1)

            # -----------------------------------
            # COLOR SELECTION
            # -----------------------------------

            if center_y < 65:

                if center_x < 100:
                    draw_color = (255,0,0)

                elif center_x < 200:
                    draw_color = (0,255,0)

                elif center_x < 300:
                    draw_color = (0,0,255)

                elif center_x < 400:
                    draw_color = (0,255,255)

                elif center_x > 500:
                    canvas = np.zeros((480,640,3),
                                      dtype=np.uint8)

       

            else:

                if prev_x == 0 and prev_y == 0:
                    prev_x = center_x
                    prev_y = center_y

                cv.line(canvas,
                        (prev_x, prev_y),
                        (center_x, center_y),
                        draw_color,
                        5)

                prev_x = center_x
                prev_y = center_y

    else:
        prev_x = 0
        prev_y = 0

    combined = cv.add(frame, canvas)

    cv.imshow("Finger Virtual Painter", combined)

    if cv.waitKey(1) & 0xFF == ord('d'):
        break

camera.release()
cv.destroyAllWindows()