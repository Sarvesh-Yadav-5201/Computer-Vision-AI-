import cv2
import mediapipe as mp
import time

# Importing the pose detection module we created:
import pose_module as pmd

# Capturing the Video:
cap  = cv2.VideoCapture('DATA/video3.mp4')

# Creating a poseDetector object here for the class
detector = pmd.PoseDetector()

prev_time = 0
while True:
    
    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break
        
    # getting the pose 
    image = detector.findPose(image)
    # getting the list of landmarks:
    lm_list = detector.findlandmarks(image)

    if len(lm_list) !=0:
        print(lm_list[23])
    # Putting up the FPS on the image :
    cur_time = time.time()
    fps = 1/(cur_time - prev_time)
    prev_time = cur_time
    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    # Display the captured frame
    cv2.imshow('image', image)

    key = cv2.waitKey(4)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()