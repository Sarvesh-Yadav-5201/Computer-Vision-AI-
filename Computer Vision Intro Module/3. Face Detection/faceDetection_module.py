import cv2
import mediapipe as mp
import time 

class face_detection():
    def __init__(self,min_confidence_score = 0.5):

        self.score = min_confidence_score

        # FOR FACE DETECTION MODEULS :
        self.mpFaceDetection =  mp.solutions.face_detection
        self.face_detection = self.mpFaceDetection.FaceDetection(self.score)
        self.mpDraw = mp.solutions.drawing_utils



    def find_faces(self, image , draw =True):

        # If we want to work to work with mediapipe, we need to convert our frames from BGR to RGB:
        RGBimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results= self.face_detection.process(RGBimage)
        # print (results.detections)

        boxes = []
        # There might be multiple Faces :
        if self.results.detections:
            for id,detection in enumerate (self.results.detections):
                ''' 
                # To draw squares  around the faces : direct function
                # mpDraw.draw_detection(image,detection )

                # print (id,detection)      # To get the whole Info about the detection 
                # print (id, detection.score) # to get the confidence score of the model
                # print (id, detection.location_data.relative_bounding_box) # to get the info for bounding box (normalized form)
                '''
                b_box = detection.location_data.relative_bounding_box  # this holds the info about the bounding box
                # denormalizing the pixel value image 
                height , width, _ = image.shape

                bbox  = int(b_box.xmin * width) , int(b_box.ymin * height),\
                        int(b_box.width * width) , int(b_box.height * height)
                boxes.append ([id, bbox,detection.score[0]*100])

                if draw == True:
                    image  = self.fancy_draw(image, bbox)

                    cv2.putText(image,f'{str(int(detection.score[0]*100))} %',(bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),2 )
                # From this function we want to return id, bounding box vallues, and confidence score.

        return image, boxes
   
    def fancy_draw(self, image, bbox, l = 30, t = 5):
        x1,y1,w,h = bbox
        x2 , y2 =  x1+w, y1+h

        # Printing the rectangle on the faces by our own cv2 model:
        cv2.rectangle(image, bbox, (255,0,0),1)

        # for left upper corner
        cv2.line(image, (x1,y1), (x1 + l, y1), (0,0,255),t)
        cv2.line(image, (x1,y1), (x1, y1+l), (0,0,255),t)

        # for right upper corner
        cv2.line(image, (x2,y1), (x2 - l, y1), (0,0,255),t)
        cv2.line(image, (x2,y1), (x2, y1+l), (0,0,255),t)

        # for left bottom corner
        cv2.line(image, (x1,y2), (x1 + l, y2), (0,0,255),t)
        cv2.line(image, (x1,y2), (x1, y2-l), (0,0,255),t)

        # for right upper corner
        cv2.line(image, (x2,y2), (x2 - l, y2), (0,0,255),t)
        cv2.line(image, (x2,y2), (x2, y2-l), (0,0,255),t)
        return image

def main():
    # Capturing the Video Frames :
    cap = cv2.VideoCapture('DATA/video1.mp4')
    # cap = cv2.VideoCapture(0)

    # object of our class:
    detector = face_detection()

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


if __name__ == '__main__':
    main()