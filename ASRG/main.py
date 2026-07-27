import cv2 as cv
import time
import numpy as np
from ASRG.aruco_utils import initDetector,detectAruco,calcAngle
from ASRG.detection_utils import filtered_componets

def main():
    #cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap = cv.VideoCapture(r"ASRG\HZ_Kto.mp4")
    frame = cap.read()[1]
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    last_frame = np.zeros_like(gray_frame, dtype=frame.dtype)

    detector = initDetector()
    while True:
        start = time.time()
        _,frame = cap.read()
        corners, idx, rejected = detectAruco(detector,frame)
        if not(idx is None):
            for i, id in enumerate(idx):
                if id == 0:
                    angle = calcAngle(corners[i])
                    #print(int(angle))
        
        blur_frame = cv.GaussianBlur(frame,ksize=(9,9), sigmaX=0)
        gray_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2GRAY)
        diff_frame = cv.absdiff(gray_frame, last_frame)
        _, motion = cv.threshold(diff_frame, 25,255, cv.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        motion = cv.dilate(motion, kernel, iterations=3)
        last_frame = gray_frame.copy()
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
            motion, connectivity=8)

        filtered_stats = filtered_componets(stats)
        for stats in filtered_stats:
            cv.rectangle(motion,pt1=(stats[0],stats[1]),pt2=(stats[0]+stats[2],stats[1]+stats[3]),color=(255,255,255),thickness=5 )
        cv.imshow("frame", motion)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()