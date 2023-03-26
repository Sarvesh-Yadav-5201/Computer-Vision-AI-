import cv2
import mediapipe as mp
import time 


# Capturing the Video Frames :
cap = cv2.VideoCapture('DATA/video4.mp4')
# cap = cv2.VideoCapture(0)

# FOR FACE DETECTION MODEULS :
mpFaceDetection =  mp.solutions.face_detection
face_detection = mpFaceDetection.FaceDetection()
mpDraw = mp.solutions.drawing_utils

# to get the frames on the screen
p_time = 0
while True:

    success , image = cap.read()
    # Checking if the frame is successfully captured
    if not success:
        print ('Unable to read Frames')
        break
    
    # If we want to work to work with mediapipe, we need to convert our frames from BGR to RGB:
    RGBimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results= face_detection.process(RGBimage)
    # print (results.detections)

    # There might be multiple Faces :
    if results.detections:
        for id,detection in enumerate (results.detections):
            # To draw squares  around the faces : direct function
            # mpDraw.draw_detection(image,detection )

            # print (id,detection)      # To get the whole Info about the detection 
            # print (id, detection.score) # to get the confidence score of the model
            # print (id, detection.location_data.relative_bounding_box) # to get the info for bounding box (normalized form)

            b_box = detection.location_data.relative_bounding_box  # this holds the info about the bounding box
            # denormalizing the pixel value image 
            height , width, _ = image.shape

            bbox  = int(b_box.xmin * width) , int(b_box.ymin * height),\
                    int(b_box.width * width) , int(b_box.height * height)

            # Printing the rectangle on the faces by our own cv2 model:
            cv2.rectangle(image, bbox, (255,0,255),2)
            cv2.putText(image,f'{str(int(detection.score[0]*100))} %',(bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),2 )


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