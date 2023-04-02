import cv2
import mediapipe as mp
import time

# Read the image/ Video
cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands  = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils

# To get the frame Rates :
prev_time =  0
cur_time = 0


while True:

    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break

    # To work with mediapipe , we need to convert the img from BGR to RGB
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Getting the results(for palms) by analyzing the frames 
    results = hands.process(imgRGB)
    # print (results) # Its working :)

    if results.multi_hand_landmarks:
        for handlm in results.multi_hand_landmarks:
            for id , lm in enumerate(handlm.landmark):
                height, width, _ = image.shape
                # print (id, lm) # its working :)
                cx , cy= int(lm.x *width) , int(lm.y*height)
                # print (id,cx,cy)

                if id == 12: # track tip of middle finger
                    cv2.circle(image, (cx,cy), 15, (255,0,255), cv2.FILLED)
                if id == 4: # track tip of the thumb
                    cv2.circle(image, (cx,cy), 15, (255,200,255), cv2.FILLED)
            mpDraw.draw_landmarks(image, handlm, mphands.HAND_CONNECTIONS)

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