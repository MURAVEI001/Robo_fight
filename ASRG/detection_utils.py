import cv2 as cv
import numpy as np

def filterComponents(stats, threshold):
    filtered_stats = []

    for i, stat in enumerate(stats): 
        if i == 0:
            continue
        if stat[4] > threshold:
            filtered_stats.append(stat)
    return filtered_stats

def getROI(frame, points_self,offset=0):
    centr_point = points_self[2] + ((points_self[0] - points_self[2])//2)
    ROI = np.array([centr_point - offset, centr_point + offset])
    return ROI

def drawAngle(frame,angle):
    frame = cv.putText(frame, text=f"Angle: {angle}",org=([40,60]),fontFace=1,fontScale=5,color=(0,0,255),thickness=5)
    return frame

def drawSelf(frame,self_position):
    frame = cv.line(frame, pt1=self_position[0],pt2=self_position[1],color=(0,0,255),thickness=3)
    frame = cv.line(frame, pt1=self_position[1],pt2=self_position[2],color=(0,0,255),thickness=3)
    frame = cv.line(frame, pt1=self_position[2],pt2=self_position[3],color=(0,0,255),thickness=3)
    frame = cv.line(frame, pt1=self_position[3],pt2=self_position[0],color=(0,0,255),thickness=3)
    frame = cv.line(frame, pt1=self_position[0],pt2=self_position[2],color=(255,0,0),thickness=3)

    return frame