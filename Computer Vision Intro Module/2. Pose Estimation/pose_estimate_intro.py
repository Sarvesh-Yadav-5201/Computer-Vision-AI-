# importing the libraries :
import cv2
import mediapipe as mp
import time 

# Capturing the Video:
cap  = cv2.VideoCapture('DATA/video1.mp4')

# Initializing the Pose detection model:
mpPose = mp.solutions.pose
pose= mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

prev_time = 0
while True:
    
    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break

    # To work with mediapipe , we need to convert the img from BGR to RGB
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            height , width,_ = image.shape
            cx , cy = int(lm.x*width), int(lm.y*height)
            print (id, cx,cy)
            
            # generating circles on hips specified landmark :
            if id == 23 or id == 24:
                cv2.circle(image, (cx,cy), 10, (255,255,0), cv2.FILLED)


    mpDraw.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS)


    
    # Putting up the FPS on the image :
    cur_time = time.time()
    fps = 1/(cur_time - prev_time)
    prev_time = cur_time
    cv2.putText(image,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    # Display the captured frame
    cv2.imshow('image', image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()