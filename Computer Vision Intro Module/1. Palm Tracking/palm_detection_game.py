import cv2
import mediapipe as mp
import time
# MODEL IMPORT 
import hand_tracking_module as htm


# Read the image/ Video
cap = cv2.VideoCapture(0)   

# To get the frame Rates :
prev_time =  0
cur_time = 0

# Creating the detector object
detector = htm.HandDetector()

while True:
    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break
    
    image  = detector.findHands(image)

    # Getting the list of landmark for particular hand:
    lm_list = detector.findPosition(image)

    if len(lm_list) !=0:
        print (lm_list[12])
    # Putting up the FPS on the image :
    cur_time = time.time()
    fps = 1/(cur_time - prev_time)
    prev_time = cur_time

    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    # Display the captured frame
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
