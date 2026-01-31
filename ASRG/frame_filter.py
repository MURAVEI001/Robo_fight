import cv2 as cv
import numpy as np

def getHsvFrame(frame):
    filter = np.array([[0,50,120],[255,255,206]])
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV_FULL)
    mask = cv.inRange(hsv_frame, filter[0], filter[1])
    return cv.bitwise_or(frame,frame, mask=mask)

def getRedFrame(frame):
    frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV_FULL)
    red = np.array([[[180,1,1],[255,255,255]],[[0,1,1],[40,255,255]]])
    mask1 = cv.inRange(frame,red[0][0],red[0][1])
    mask2 = cv.inRange(frame,red[1][0],red[1][1])
    return cv.bitwise_or(mask1,mask2)

def getGreenFrame(frame):
    frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV_FULL)
    green = np.array([[50,0,0],[120,255,255]])
    return cv.inRange(frame,green[0],green[1])