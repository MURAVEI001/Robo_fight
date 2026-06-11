import cv2 as cv

def getCap(numCam):
    capList = []
    for i in range(numCam):
        capList.append(cv.VideoCapture(i))
    return capList

def getFrame(capList):
    frameDict = {}
    for i, cap in enumerate(capList):
         _, frameDict[f"{i}"] = cap.read()
    return frameDict