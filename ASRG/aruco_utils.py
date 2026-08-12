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

def getPointsMarker(corners):
    corners = corners.squeeze()
    points = corners.astype(np.int32)
    return points

def calcAngle(corners):
    corners = corners[0]
    p1 = corners[1]
    p3 = corners[3]
        
    vec_x = p3[0] - p1[0]
    vec_y = p3[1] - p1[1]
    
    angle_in_rad = np.arctan2(vec_x,vec_y)
    angle = np.degrees(angle_in_rad)
    
    return angle