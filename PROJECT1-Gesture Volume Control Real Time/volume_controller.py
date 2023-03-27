# importing the libraries:
import cv2
import time
import numpy as np
import math
#___________________________________________
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#___________________________________________________________
# importing our hand_tracking module :
import hand_tracking_module as htm 

##############################################################
# PARAMETERS :

cam_width , cam_height = 400 , 400

# FROM PYCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range = (volume.GetVolumeRange())

# our volume Range is (-63.5, 0.0)
min_vol = vol_range[0]
max_vol = vol_range[1]
vol = 0
vol_bar = 400
vol_per = 0

##############################################################

# initializing the cv2 module to capture the Video:
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)   # This controls the width of the frame
cap.set(4, cam_height)  # This controls the height of the frame.

# Initializing our palm-detector module:
detector = htm.HandDetector()

p_time = 0
while True:
    success, image = cap.read()
    if success == None:
        print ('Unable to Capture the Frame')
        break
    
    image  = detector.findHands(image)

    # Now lets get the landmarks:
    lm_list = detector.findPosition(image, draw = True)
    if len(lm_list) >0:
        # print (lm_list[4], lm_list[8]) # This will show the landmark for tip of the thumb and index finger.
        x1, y1 = lm_list[4][1:]  # X and y co-ordinate for the tip of thumb
        x2, y2 = lm_list[8][1:]  # X and y co-ordinate for the tip of index fingerer

        # Getting the center of this line/ tips:
        cx , cy = (x1+x2)//2, (y1+y2)//2

        # highlighting the tips
        cv2.circle(image, (x1,y1), 5, (0,0,255), cv2.FILLED)
        cv2.circle(image, (x2,y2), 5, (0,0,255), cv2.FILLED)
        cv2.circle(image, (cx,cy), 5, (0,0,255), cv2.FILLED)
        # Creating a straight line between these tips:
        cv2.line(image, (x1,y1), (x2,y2) , (255,255,0), 2)

        # Getting the length of the straight line joining the tips:
        # We will be using hypotenous function from math library:
        length = math.hypot(x2-x1, y2-y1)
        # print(length)
        # hand range minimum = 40 and maximum  = 300
        # Vol range = -65.5 (min) to 0(max)

        # We will use Numpy to scale/ interpolate our hand range length to volume range.
        vol_level = np.interp(length, [50, 250], [min_vol, max_vol])
        vol_bar   = np.interp(length, [50,250], [400,150])
        vol_per   = np.interp(length, [50,250], [0,100])

        # print (length, "--> ", vol_level)
        # And finally we will set our master volume level:
        volume.SetMasterVolumeLevel(vol_level, None)

        if length <= 40:
            # we change the color of center circle:
            cv2.circle(image, (cx,cy), 8, (0,255,255), cv2.FILLED)

    cv2.rectangle(image, (48, 148), (87, 402), (0,0,0),2)    
    cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (0,255,0),cv2.FILLED)    
    cv2.putText(image,f'{int(vol_per)}%', (40,450), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)


    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time
    cv2.putText(image,f'FPS : {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
    cv2.imshow('Video', image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
