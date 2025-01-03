import cv2
import numpy as np

class BackgroundSubtractor:
    def __init__(self, alpha=0.001):
        self.alpha = alpha
        self.background = None
        #testing

    def apply(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0) 

        if self.background is None:
            self.background = gray.copy().astype("float")


        diff = cv2.absdiff(gray, cv2.convertScaleAbs(self.background))
       

       
        cv2.accumulateWeighted(gray, self.background, self.alpha)

       
        diff = cv2.absdiff(gray, cv2.convertScaleAbs(self.background))

     
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        return thresh

