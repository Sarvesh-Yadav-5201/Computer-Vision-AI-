# importing the libraries :
import cv2
import mediapipe as mp
import time 


class PoseDetector():
    def __init__(self, mode = False, upBody = False, smooth  = True, 
                 detectionCon= 0.5, trackingCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        # Initializing the Pose detection model:
        self.mpPose = mp.solutions.pose
        self.pose= self.mpPose.Pose(self.mode, self.upBody, 
                                    self.smooth)
        self.mpDraw = mp.solutions.drawing_utils


    def findPose(self, image, draw = True):
        # To work with mediapipe , we need to convert the img from BGR to RGB
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(image, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return image

    def findlandmarks(self, image, draw = True):
        lm_list = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                height , width,_ = image.shape
                cx , cy = int(lm.x*width), int(lm.y*height)

                lm_list.append([id, cx, cy])

                if draw:
                    cv2.circle(image, (cx,cy), 3, (255,255,0), cv2.FILLED)

        return lm_list

# dummy code for the module:
def main():
    
    # Capturing the Video:
    cap  = cv2.VideoCapture('DATA/video1.mp4')

    # Creating a poseDetector object here for the class
    detector = PoseDetector()

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

if __name__ == '__main__':
    main()