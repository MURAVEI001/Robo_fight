import cv2 as cv

def joinedFrame(frameDict):
    v1 = cv.vconcat([frameDict["0"], frameDict["2"]])
    v2 = cv.vconcat([frameDict["1"], frameDict["3"]])
    joinFrame = cv.hconcat([v1,v2])
    return joinFrame