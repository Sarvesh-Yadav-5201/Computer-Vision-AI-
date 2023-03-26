# importing the libraries 
import cv2
import mediapipe as mp
import time 
# importing the face detection module we created
import faceDetection_module as fdm

# Capturing the Video Frames :
cap = cv2.VideoCapture('DATA/video1.mp4')
# cap = cv2.VideoCapture(0)

# object of our class:
detector = fdm.face_detection()

# to get the frames on the screen
p_time = 0
while True:

    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break
    
    image , b_boxes = detector.find_faces(image)   # If we want to draw the squares around the faces 
    # image , b_boxes = detector.find_faces(image, draw  = False) # If we don't want to draw the squares around the faces 

    # If we want, we can print the bounding boxes:
    print (b_boxes)

        # Showing the fps on the screen:
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time

    cv2.putText(image,f' FPS: {str(int(fps))}',(10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3 )

    cv2.imshow('image', image)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()