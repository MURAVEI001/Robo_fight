import cv2 as cv
import time
import numpy as np
from ASRG.aruco_utils import initDetector,detectAruco,calcAngle, getPointsMarker
from ASRG.detection_utils import filterComponents, drawAngle, drawSelf, getROI
from ASRG.fps import showFPS

def main():
    cap = cv.VideoCapture(r"ASRG\4.mp4")
    _, frame = cap.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    last_frame = np.zeros_like(gray_frame, dtype=frame.dtype)

    detector = initDetector()

    times = []
    angle = None
    points_self = None
    while True:
        start = time.time()
        _, frame = cap.read()
        aruco_flag = False
        corners, ids, rejected = detectAruco(detector,frame)
        if not(ids is None):
            for i, id in enumerate(ids):
                if id == 47 :
                    angle = calcAngle(corners[i])
                    points_self = getPointsMarker(corners[i])
                    aruco_flag = True
                    break

        if aruco_flag:
            ROI = getROI(frame,points_self, offset=100)
            cv.rectangle(frame,pt1=(ROI[0]),pt2=(ROI[1]),color=(0,255,0),thickness=9)

            #frame = frame[ROI[0][1]:ROI[1][1], ROI[0][0]:ROI[1][0]]
      
        # blur_frame = cv.GaussianBlur(frame,ksize=(9,9), sigmaX=0)
        # gray_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2GRAY)
        # last_frame = np.zeros_like(gray_frame, dtype=frame.dtype)

        # diff_frame = cv.absdiff(gray_frame, last_frame)
        # _, threshold = cv.threshold(diff_frame, 60,255, cv.THRESH_BINARY)
        # kernel = np.ones((3, 3), np.uint8)
        # motion = cv.dilate(threshold, kernel, iterations=3)
        # last_frame = gray_frame.copy()
        # num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
        #     motion, connectivity=8)

        # filtered_stats = filterComponents(stats, 1200)

        # #frame = drawAngle(frame, angle)
        # for stats in filtered_stats:
        #     pt1 = np.array([stats[0],stats[1]])
        #     pt2 = np.array([stats[0]+stats[2],stats[1]+stats[3]])
        #     self_position = np.array([pt1,pt2])
        # frame = drawSelf(frame, self_position=points_self)

        cv.imshow("frame", frame)
        #cv.imshow("frame1", threshold)

        showFPS(times,start)

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()