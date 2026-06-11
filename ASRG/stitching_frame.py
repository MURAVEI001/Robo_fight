import cv2 as cv

def joinedFrame(frameDict):
    if len(frameDict) > 1:
        joinFrame = cv.hconcat([frameDict["0"],frameDict["1"]])
    else:
        joinFrame = frameDict["0"]
    return joinFrame 