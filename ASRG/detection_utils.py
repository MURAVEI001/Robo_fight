import cv2 as cv
import numpy as np

def filterComponets(stats, threshold):
    filtered_stats = []

    for i, stat in enumerate(stats): 
        if i == 0:
            continue
        if stat[4] > threshold:
            filtered_stats.append(stat)
    return filtered_stats

def getROI(frame,offset=0):
    pass

def updateHistory(aruco=None,xySelf=None,xyEnemy=None):
    pass

def drawInfo(frame,angle=None,xySelf=None,xyEnemy=None, drawAngle=False, drawSelf=False, drawEnemy=False):
    if drawSelf and not(xySelf is None):
        frame = cv.rectangle(frame,pt1=xySelf[0],pt2=xySelf[1],color=(0,0,255),thickness=5)
    if drawAngle and not(angle is None):
        frame = cv.putText(frame, text=f"Angle: {angle}",org=([40,60]),fontFace=1,fontScale=5,color=(0,0,255),thickness=5)
    return frame