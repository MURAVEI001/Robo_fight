import numpy as np
from cv2 import aruco

def initDetector():
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)
    return detector

def detectAruco(detector, frame):
    corners, id, rejected = detector.detectMarkers(frame)
    return corners, id, rejected

def calcAngle(corners):
    corners = corners[0]
    p0 = corners[3]
    p1 = corners[0]
        
    dx = p0[0] - p1[0]
    dy = p0[1] - p1[1]

    angle_rad = np.arctan2(dx,dy)
    angle = np.degrees(angle_rad)
    return angle