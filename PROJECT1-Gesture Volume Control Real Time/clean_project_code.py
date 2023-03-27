# Import necessary libraries
import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import hand_tracking_module as htm   # Import hand tracking module

# Set camera parameters
CAM_WIDTH, CAM_HEIGHT = 400, 400

# Get audio device and volume information using pyCaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
MIN_VOL, MAX_VOL = vol_range[0], vol_range[1]

# Initialize variables for volume control
vol, vol_bar, vol_per = 0, 400, 0

# Initialize OpenCV video capture object
cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

# Initialize hand detector object
detector = htm.HandDetector()

# Initialize time variables for FPS calculation
p_time = 0

# Main loop to capture video and perform hand tracking
while True:
    # Read in a frame from the camera
    success, image = cap.read()
    if not success:
        print('Unable to capture frame')
        break

    # Use hand detector to find hands and landmarks in the frame
    image = detector.findHands(image)
    lm_list = detector.findPosition(image, draw=True)

    # Check if any landmarks were detected
    if len(lm_list) > 0:
        # Get positions of thumb and index finger tips
        x1, y1 = lm_list[4][1:]
        x2, y2 = lm_list[8][1:]

        # Calculate center point between thumb and index finger tips
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        # Draw circles around the thumb and index finger tips, and the center point
        cv2.circle(image, (x1,y1), 5, (0,0,255), cv2.FILLED)
        cv2.circle(image, (x2,y2), 5, (0,0,255), cv2.FILLED)
        cv2.circle(image, (cx,cy), 5, (0,0,255), cv2.FILLED)

        # Draw a line between the thumb and index finger tips
        cv2.line(image, (x1,y1), (x2,y2), (255,255,0), 2)

        # Calculate length of line between thumb and index finger tips
        length = math.hypot(x2-x1, y2-y1)

        # Scale hand range length to volume range using numpy interpolation
        vol_level = np.interp(length, [50, 250], [MIN_VOL, MAX_VOL])
        vol_bar = np.interp(length, [50, 250], [400, 150])
        vol_per = np.interp(length, [50, 250], [0, 100])

        # Set master volume level based on hand range length
        volume.SetMasterVolumeLevel(vol_level, None)

        # Change color of center circle if hand range length is less than 40
        if length <= 40:
            cv2.circle(image, (cx,cy), 8, (0,255,255), cv2.FILLED)

    # Draw volume bar on screen
    cv2.rectangle(image, (48, 148), (87, 402), (0,0,0),2)    
    cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (0,255,0),cv2.FILLED)    
    cv2.putText(image,f'{int(vol_per)}%', (40,450), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    # Print FPS on the Screen
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time
    cv2.putText(image,f'FPS : {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)

    # Showing the Frames 
    cv2.imshow('Video', image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

