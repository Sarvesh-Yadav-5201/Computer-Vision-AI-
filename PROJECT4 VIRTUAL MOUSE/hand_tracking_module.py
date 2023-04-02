import cv2
import mediapipe as mp
import time
import math

# WE can use this module for other projects as well.


class HandDetector():
    # initializing setup for the module 
    def __init__(self, mode=False, maxHands=2 ,detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = int(detectionCon * 100)  # Convert to integer
        self.trackingCon = int(trackingCon * 100)  # Convert to integer

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode) #, max_num_hands =self.maxHands,min_detection_confidence = self.detectionCon,min_tracking_confidence = self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        # Specifying the landmark indices for the fingertips: 8 : index, 12: middle, 16: ring, 20: pinky
        self.tip_ids = [8,12,16,20]  

    # This module will help us to determine the hands 
    def findHands (self, image, draw = True):

        # To work with mediapie , we need to convert the img from BGR to RGB
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Getting the results(for palms) by analyzing the frames 
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlm in self.results.multi_hand_landmarks:
                if draw == True:
                    self.mpDraw.draw_landmarks(image, handlm, self.mphands.HAND_CONNECTIONS)

        return image

    def findPosition (self, image, handNo = 0, draw = False):
        # list to contain all the landmarks values for a particular hand
        self.lm_list = []

        if self.results.multi_hand_landmarks: 
            hand = self.results.multi_hand_landmarks[handNo]

            for id , lm in enumerate(hand.landmark):
                height, width, _ = image.shape
                cx , cy= int(lm.x *width) , int(lm.y*height)
                # print (id, cx, cy) # its working :)
                self.lm_list.append([id,cx,cy])

                if draw:
                    cv2.circle(image, (cx,cy), 5, (255, 0, 0), cv2.FILLED)
        
        return self.lm_list
    
    def fingers_up(self):
        fingers = []

        # Checking for the thumb
        if self.lm_list[0][1] >= self.lm_list[1][1]:
            if self.lm_list[4][1] <= self.lm_list[2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if self.lm_list[4][1] <= self.lm_list[2][1]:
                fingers.append(0)
            else:
                fingers.append(1)

        # Checking for the four fingers
        for id in self.tip_ids: 
            if self.lm_list[id][2] <= self.lm_list[id-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


    def find_distance(self, p1, p2, image, draw = True, r= 15, t= 3):
        x1,y1 = self.lm_list[p1][1:]
        x2,y2 = self.lm_list[p2][1:]

        cx,cy = (x1+x2) //2 , (y1 + y2)//2

        if draw:
            cv2.line(image, (x1,y1), (x2,y2),(255,0,255),t)
            cv2.circle(image, (x1,y1), r,(255,0,255), cv2.FILLED)
            cv2.circle(image, (x2,y2), r,(255,0,255), cv2.FILLED)
            cv2.circle(image, (cx,cy), r,(255,0,255), cv2.FILLED) 

        length = math.hypot(x2-x1 , y2-y1)

        return length , image, [x1,y1 , x2,y2, cx,cy]
#________________________________________________________________________________________


# main function to rum the whole Module
def main():
    # Read the image/ Video
    cap = cv2.VideoCapture(0)   

    # To get the frame Rates :
    prev_time =  0
    cur_time = 0

    # Creating the detector object
    detector = HandDetector()

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
            # print (lm_list[12])
            pass


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



if __name__ == '__main__':
    main()



