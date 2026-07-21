import cv2 as cv
import numpy as np
from cv2 import aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

detector = aruco.ArucoDetector(dictionary, parameters)

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    corners, id, rejected = detector.detectMarkers(frame)
    try:
        corners = corners[0][0]
        p0 = corners[3]
        p1 = corners[0]
        
        dx = p0[0] - p1[0]
        dy = p0[1] - p1[1]

        angle_rad = np.arctan2(dx,dy)
        angle = np.degrees(angle_rad)

        print(angle)
    except:
        pass

    cv.imshow("frame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()