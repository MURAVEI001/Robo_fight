import cv2 as cv
import time

def getCap(numCam):
    capList = []
    for i in range(numCam):
        capList.append(cv.VideoCapture(i, cv.CAP_DSHOW))
        capList[i].set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        capList[i].set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    return capList

def getFrame(capList):
    frameDict = {}
    for i, cap in enumerate(capList):
        _, frame = cap.read()
        frameDict[f"{i}"] = cv.resize(frame, (1920, 1080), interpolation=cv.INTER_LINEAR)
    return frameDict