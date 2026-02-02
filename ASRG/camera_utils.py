import cv2 as cv

def getCap(numCam):
    capList = []
    for i in range(numCam):
        capList.append(cv.VideoCapture(i, cv.CAP_MSMF))
        capList[i].set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        capList[i].set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        capList[i].set(cv.CAP_PROP_FPS,30)
    return capList

def getFrame(capList):
    frameDict = {}
    for i, cap in enumerate(capList):
         _, frameDict[f"{i}"] = cap.read()
    return frameDict