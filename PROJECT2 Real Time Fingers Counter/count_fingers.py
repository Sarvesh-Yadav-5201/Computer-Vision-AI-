# Importing required libraries
import cv2
import numpy as np
import mediapipe as mp
import time 

# Importing the HandDetector module to detect hands/palms
import hand_tracking_module as htm

# Initializing the OpenCV and HandDetector objects to capture video and start tracking palm respectively
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

# Specifying the landmark indices for the fingertips: 8 : index, 12: middle, 16: ring, 20: pinky
tip_ids = [8,12,16,20]  

# Initializing the variable to keep track of the previous time
p_time = 0

# Infinite loop to capture video frames
while True:
    # Reading the video frame
    success, image = cap.read()
    if not success:
        print('Unable to read the frames.')
        break

    # Detecting hands/palms in the video frame
    image = detector.findHands(image)

    # Retrieving the landmarks of the detected hands/palms
    lm_list = detector.findPosition(image, draw=False)
    if len(lm_list) != 0:
        id_value = []

        # Checking for the thumb
        if lm_list[0][1] >= lm_list[1][1]:
            if lm_list[4][1] <= lm_list[2][1]:
                id_value.append(1)
            else:
                id_value.append(0)
        else:
            if lm_list[4][1] <= lm_list[2][1]:
                id_value.append(0)
            else:
                id_value.append(1)

        # Checking for the four fingers
        for id in tip_ids: 
            if lm_list[id][2] <= lm_list[id-2][2]:
                id_value.append(1)
            else:
                id_value.append(0)

        # Counting the total number of open fingers
        finger_count = id_value.count(1)
        # print(finger_count)

        # Putting the finger count text on the image
        cv2.rectangle(image, (20, 225), (170,425), (0,255,255), cv2.FILLED)
        cv2.putText(image, f'{str(finger_count)}',(45, 375), cv2.FONT_HERSHEY_PLAIN,10,(0,0,250),10)

    # Calculating the FPS and putting it on the screen
    c_time = time.time()
    fps = 1/ (c_time - p_time)
    p_time = c_time
    cv2.putText(image, f'FPS: {str(int(fps))}', (10,70),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,100), 2)

    # Showing the video frame
    cv2.imshow('Video', image )

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing the camera and closing all windows
cap.release()
cv2.destroyAllWindows()
