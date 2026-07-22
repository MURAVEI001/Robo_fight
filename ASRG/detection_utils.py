import cv2 as cv
import time
import numpy as np

def main():
    cap = cv.VideoCapture(r"D:\GitHub\Robo_fight\ASRG\video2.mp4")
    frame = cap.read()[1]
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    last_frame = np.zeros_like(gray_frame, dtype=frame.dtype)

    while True:
        start = time.time()
        _, frame = cap.read()

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur_frame = cv.GaussianBlur(gray_frame, ksize=(5,5), sigmaX=0)

        diff_frame = cv.absdiff(blur_frame, last_frame)
        _, bin_frame = cv.threshold(diff_frame, 30,255,cv.THRESH_BINARY)
        last_frame = blur_frame.copy()
        contours, hierarchy = cv.findContours(bin_frame,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

        cv.imshow("frame", bin_frame)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()