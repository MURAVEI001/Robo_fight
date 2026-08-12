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

def getCentr(points_self):
    centr_point = points_self[2] + ((points_self[0] - points_self[2])//2)
    return centr_point

def getROI(centr_point, offset=0):
    ROI = np.array([centr_point - offset, centr_point + offset])
    return ROI

def drawAngle(frame,angle):
    frame = cv.putText(frame, text=f"Angle: {angle}",org=([40,60]),fontFace=1,fontScale=5,color=(0,0,255),thickness=5)
    return frame

def drawBox(frame,self_position):
    frame = cv.rectangle(frame, pt1=(self_position[0]),pt2=(self_position[1]),color=(0,0,255),thickness=3)
    return frame

def cycleDetection(frame, prev_frame):
    blur_frame = cv.GaussianBlur(frame,ksize=(5,5), sigmaX=0)
    diff_frame = cv.absdiff(blur_frame, prev_frame)
    _, threshold = cv.threshold(diff_frame, 20,255, cv.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    motion = cv.dilate(threshold, kernel, iterations=4)
    prev_frame = blur_frame.copy()
    return motion, prev_frame