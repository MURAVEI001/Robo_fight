import cv2 as cv
import time
import numpy as np

def main():
    #cap = cv.VideoCapture(r"D:\GitHub\Robo_fight\ASRG\video2.mp4")
    cap = cv.VideoCapture(r"D:\GitHub\Robo_fight\ASRG\1.jpg")
    _,frame = cap.read()
    #cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    # frame = cap.read()[1]
    #gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    last_frame = np.zeros_like(frame, dtype=frame.dtype)
    gray_last_frame = cv.cvtColor(last_frame, cv.COLOR_BGR2GRAY)


    while True:
        # start = time.time()
        # _, frame = cap.read()

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        diff_frame = cv.absdiff(gray_frame, gray_last_frame)
        _, motion = cv.threshold(diff_frame, 25,255,cv.THRESH_BINARY)
        # kernel = np.ones((3, 3), np.uint8)
        # motion = cv.dilate(motion, kernel, iterations=2)

        # last_frame = gray_frame.copy()
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(motion, connectivity=8)
        print(num_labels, "\n" , labels, "\n", stats, "\n", centroids)
        input()
        for i in range(num_labels):
            cv.line(motion,pt1=(stats[i,0],stats[i,1]),pt2=(stats[i,0]+stats[i,2],stats[i,1]+stats[i,3]),color=(255,255,255),thickness=5 )
            cv.line(motion,pt1=(int(centroids[i,0]),int(centroids[i,1])),pt2=(int(centroids[i,0]),int(centroids[i,1])),color=(0,0,0),thickness=10)
        cv.imshow("frame", motion)
        # print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()