import cv2 as cv
import time
import numpy as np
from ASRG.aruco_utils import initDetector,detectAruco,calcAngle
from ASRG.detection_utils import filterComponets, drawInfo, getROI, updateHistory

def main():
    cap = cv.VideoCapture(r"ASRG\2.mp4")
    _, frame = cap.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    last_frame = np.zeros_like(gray_frame, dtype=frame.dtype)

    detector = initDetector()
    while True:
        start = time.time()
        _, frame = cap.read()
        aruco = False
        corners, idx, rejected = detectAruco(detector,frame)
        if not(idx is None):
            for i, id in enumerate(idx):
                if id == 47 :
                    angle = calcAngle(corners[i])
                    aruco = True
        
        blur_frame = cv.GaussianBlur(frame,ksize=(9,9), sigmaX=0)
        gray_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2GRAY)
        diff_frame = cv.absdiff(gray_frame, last_frame)
        _, threshold = cv.threshold(diff_frame, 25,255, cv.THRESH_BINARY)
        kernel = np.ones((9, 9), np.uint8)
        motion = cv.dilate(threshold, kernel, iterations=2)
        last_frame = gray_frame.copy()
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
            motion, connectivity=8)

        filtered_stats = filterComponets(stats, 4000)

        for stats in filtered_stats:
            pt1 = np.array([stats[0],stats[1]])
            pt2 = np.array([stats[0]+stats[2],stats[1]+stats[3]])
            xySelf = np.array([pt1,pt2])
            frame = drawInfo(frame, xySelf=xySelf, drawSelf=True)

        cv.imshow("frame", frame)
        #print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()