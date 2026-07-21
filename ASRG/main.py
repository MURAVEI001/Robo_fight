import cv2 as cv
import time
import numpy as np

def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    
    while True:
        start = time.time()
        _,frame = cap.read()
        cv.imshow("frame", frame)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()