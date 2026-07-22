import cv2 as cv
import time
from aruco_utils import initDetector,detectAruco,calcAngle

def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    # cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
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

        cv.imshow("frame", frame)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()