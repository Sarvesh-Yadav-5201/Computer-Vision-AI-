import cv2
import mediapipe as mp
import time 
import os
import numpy as np
import hand_tracking_module as htm

# SETUP PAINT BAR:
folder_path = 'paint_bar'
my_list = os.listdir(folder_path)
overlay_list = []
for im_path in my_list:
    image = cv2.imread(f'{folder_path}/{im_path}')
    overlay_list.append(image)
header = overlay_list[0]
display_color = (0, 0, 255)

# SET UP CAPTURE:
cap = cv2.VideoCapture(0)
w_cap, h_cap = 1280, 720
cap.set(3, w_cap)
cap.set(4, h_cap)

# INITIALIZE HAND TRACKING MODULE:
detect = htm.HandDetector()

# DRAWING PARAMETERS:
xp, yp = 0, 0
brush_thickness = 20
eraser_thickness = 40

# CREATE SEPARATE CANVAS TO DRAW ON:
img_canvas = np.zeros((720, 1280, 3), np.uint8)

# INITIALIZE FPS TRACKING:
p_time = 0

while True:
    # STEP 1 : Getting the Frames 
    success, image = cap.read()

    if not success:
        print ('Unable to Read the Frames')
        break
    image = cv2.flip(image , 1) # Flipping the image horizontly.

    # STEP 2 : Gettin Hand Landmarks
    image  = detect.findHands(image)

    lm_marks = detect.findPosition(image, draw = False)
    if len(lm_marks) !=0:
        # print (lm_marks[0][1])

        # Getting the Landmarks of index and middle Finger :
        x1 , y1 = lm_marks[8][1:] # x and y co-ordinate for index finger
        x2 , y2 = lm_marks[12][1:]  # x and y cordinate for middle finger

        # STEP 3 :  Check which finger is up:
        fingers = detect.fingers_up()
        # print (fingers)

        # STEP 4 : If selection Mode (Two fingers are up ) - no need to draw
        if fingers[1] == True and fingers[2] == True: # THEN WE WILL SELECT
            xp = yp = 0
            if y1 < 110 : 
                if 570 < x1 < 700:
                    header = overlay_list[1]
                    display_color = (0,255,0)

                elif 725 < x1 < 850:
                    header = overlay_list[2]
                    display_color = (255,0,0)

                elif 1000 < x1 < 1180:
                    header = overlay_list[3]
                    display_color = (0,0,0)

                else :
                    header = overlay_list[0]
                    display_color = (0,0,255)

            # visual confirmation if you are in selection mode
            cv2.rectangle(image, (x1, y1 - 20), (x2, y2 + 20),display_color, cv2.FILLED)
            # print ('SELECTION MODE')

        # STEP 5 : If paiting Mode (One Finger up) - no need to select
        if fingers[1] ==1 and fingers[2] == False: # THEN WE WILL DRAW
            # visual confirmation if you are in Drawing mode
            cv2.circle(image, (x1,y1) , 15,display_color ,cv2.FILLED)
            # print ('Drawing Mode')
            if xp == 0 and yp == 0:
                xp, yp = x1,y1
            
            if display_color == (0,0,0):
                # ERASER PART 
                # cv2.line(image, (xp, yp), (x1,y1), display_color , eraser_thickness) # We can not draw on the frame
                cv2.line(img_canvas, (xp, yp), (x1,y1), display_color , eraser_thickness) # hance we will drar on this canvas
            
            else:
                # cv2.line(image, (xp, yp), (x1,y1), display_color , brushthickness) # We can not draw on the frame
                cv2.line(img_canvas, (xp, yp), (x1,y1), display_color , brush_thickness) # hance we will drar on this canvas

            xp, yp = x1,y1 # updating the previous point.

    ################################################################################################################################################3

    # Doing some correction in the canvas and our frames to get better results :
    # Convert the canvas image to grayscale
    imgGray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)

    # Apply binary inverse thresholding to the grayscale image
    # to obtain a binary mask of the canvas
    _, imgMask = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)

    # Convert the binary mask to a BGR image for bitwise operations
    imgMask = cv2.cvtColor(imgMask, cv2.COLOR_GRAY2BGR)

    # Use bitwise AND operation to preserve only the image pixels
    # that are not part of the canvas
    image = cv2.bitwise_and(image, imgMask)

    # Use bitwise OR operation to combine the canvas and image
    # to get the final image with the drawn object on the canvas
    image = cv2.bitwise_or(image, img_canvas)
    #################################################################################################################################################

    # Getting the FPS 
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(image, str(int(fps)), (10, 135),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)

    # Overlaying the header image on the frames
    image[0:110, 0:1280] = header

    # adding the canvas and frames onto one image:
    # image  = cv2.addWeighted(image , 0.5, imgCanvas, 0.5, 0)
    # because its a blend of two images, the color will not look bright (this idea is not good)
    cv2.imshow('image', image)
    # cv2.imshow('Canva', imgCanvas)
    
    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()
