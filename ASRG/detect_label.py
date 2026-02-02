import cv2 as cv
import numpy as np

def detectLabelBlack(frame):
    filter = np.array([[0,0,120],[255,80,255]])
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV_FULL)
    mask = cv.inRange(hsv_frame, filter[0], filter[1])
    return cv.bitwise_or(frame,frame, mask=mask)
    
    # _, threshold = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    # contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
    # for i, contour in enumerate(contours):
    #     approx = cv.approxPolyDP(contour, 0.1 * cv.arcLength(contour, True), True)
        
    #     if len(approx) == 4:
    #         cv.drawContours(frame, [contour], 0, (0, 0, 255), 5)
    # return frame

def detectLabelWhite(frame):
    pass