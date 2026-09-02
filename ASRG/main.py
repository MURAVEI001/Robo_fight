import cv2 as cv
import time
import numpy as np
from ASRG.aruco_utils import initDetector,detectAruco,calcAngle, getPointsMarker
from ASRG.detection_utils import filterComponents, drawAngle, drawBox, getROI, getCentr, cycleDetection
from ASRG.fps import showFPS

# НУЖНО ОПРЕДЕЛИТЬ
# 1 ПОЛОЖЕНИЕ АРУКО
# 2 УГОЛ РОБОТА
# 3 ЕСЛИ АРУКО НЕ ОПРЕДЕЛЕНА, ТО ПОЛОЖЕНИЕ СЕБЯ
# 4 ПОЛОЖЕНИЕ ПРОТИВНИКА

def main():
    cap = cv.VideoCapture(r"ASRG/4.mp4")

    detector = initDetector()

    times = []
    angle = None
    points_self = None
    prev_frame = None
    while True:
        start = time.time()

        _, frame = cap.read()
        h, w, c = frame.shape
        frame = frame[40:h-822, 120:w-306]
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if prev_frame is None:
            prev_frame = np.zeros_like(gray_frame, dtype=gray_frame.dtype)

        motion, prev_frame = cycleDetection(gray_frame, prev_frame)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
            motion, connectivity=8)
        filtered_stats = filterComponents(stats, 500)
        for stats in filtered_stats:
            pt1 = np.array([stats[0],stats[1]])
            pt2 = np.array([stats[0]+stats[2], stats[1]+stats[3]])
            position = np.array([pt1,pt2])
            frame = drawBox(frame, position)

        # aruco_flag = False
        # corners, ids, rejected = detectAruco(detector, frame)
        # if not(ids is None):
        #     for i, id in enumerate(ids):
        #         if id == 47 :
        #             angle = calcAngle(corners[i]) # УГОЛ ПОВОРОТА
        #             points_self = getPointsMarker(corners[i])
        #             aruco_flag = True
        #             centr_point = getCentr(points_self) # ПОЛОЖЕНИЕ АРУКО
        #             cv.line(frame,pt1=centr_point,pt2=centr_point,color=(0,0,255),thickness=20)
        #             break

        # if aruco_flag:
        #     centr_point = getCentr(points_self) # ПОЛОЖЕНИЕ АРУКО

        #     motion, prev_frame = cycleDetection(gray_frame, prev_frame)

        #     num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
        #         motion, connectivity=8)

        #     filtered_stats = filterComponents(stats, 500)

        # #frame = drawAngle(frame, angle)
        #     for stats in filtered_stats:
        #         pt1 = np.array([stats[0],stats[1]])
        #         pt2 = np.array([stats[0]+stats[2],stats[1]+stats[3]])
        #         enemy_position = np.array([pt1,pt2])
        #         frame = drawBox(frame, enemy_position)

        cv.imshow("frame", frame)
        cv.imshow("frame1", motion)

        showFPS(times,start)

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()