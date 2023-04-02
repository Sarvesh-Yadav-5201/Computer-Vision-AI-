# importing the libraries:
import cv2
import mediapipe as mp
import time 


# inititating the OpenCV module to capture the frames:
# cap = cv2.VideoCapture('DATA/video3.mp4')
cap = cv2.VideoCapture(0)

# Initializing the mediapipe module to get the mesh on to the face:
mpFaceMesh = mp.solutions.face_mesh
FaceMesh = mpFaceMesh.FaceMesh(max_num_faces  = 2)        # parameters : static_image_mode, max_num_faces, min_detection_con, min_tracking_con

mpDraw = mp.solutions.drawing_utils
draw_specs = mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)
# variable to initialize the time (previous)
p_time=  0

while True:
    success, image = cap.read()
    if success == None:
        print ('Unable to read the frames')
        break

    # We want to work with medipipe module then, we need to convert the BGR image to RGB:
    RGBimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = FaceMesh.process(RGBimage)
    # print (results)

    # We may have more than one face in the frame:
    # THERE ARE A TOTAL OF 468 LANDMARKS FOR 1 PARTICULAR FACE
    if results.multi_face_landmarks:
        for id, lm in enumerate(results.multi_face_landmarks):
            # print (id, lm)
            mpDraw.draw_landmarks(image, lm, mpFaceMesh.FACEMESH_TESSELATION, draw_specs, draw_specs)

            # Getting the height and weidth of input image:
            h, w,_ = image.shape
            # Getting every single Face landmark :
            for id, l_mark in enumerate(lm.landmark):
                x ,y = int(l_mark.x*w)  , int(l_mark.y *h)
                print (id,x,y)

    # putting the fps in the frames :
    c_time = time.time()
    fps = str(int(1/(c_time - p_time)))
    p_time  = c_time
    cv2.putText(image, f'FPS: {fps}',(10,80),cv2.FONT_HERSHEY_PLAIN, 2, (0,150,200), 2)

    # Display the captured frame
    cv2.imshow('image', image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()