import cv2
import mediapipe as mp
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Constants
min_detection_confidence = 0.7
min_tracking_confidence = 0.5

# Set up camera
cap = cv2.VideoCapture(0)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Get video input size
_, frame = cap.read()
input_height, input_width, _ = frame.shape
input_shape = (input_height, input_width)

# Initialize hand tracking
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to pass by reference
        image.flags.writeable = False

        # Process image and get hand landmarks
        results = hands.process(image)

        # Draw landmarks on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Get index finger landmark
                index_finger_landmark = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]

                # Get x,y coordinates
                index_finger_x = int(index_finger_landmark.x * input_width)
                index_finger_y = int(index_finger_landmark.y * input_height)

                # Convert to screen coordinates
                x = int(index_finger_x * (screen_width / input_width))
                y = int(index_finger_y * (screen_height / input_height))

                # Move the mouse
                pyautogui.moveTo(x, y)

        # Show the image
        cv2.imshow("Virtual Mouse", image)

        # Exit if 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

# Release the webcam
cap.release()

# Close all windows
cv2.destroyAllWindows()
