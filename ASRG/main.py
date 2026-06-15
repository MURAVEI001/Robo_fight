import cv2 as cv
import time
import numpy as np
from camera_utils import getCap, getFrame
from stitching_frame import joinedFrame

def main():
    #capList = getCap(1)
    #cap = cv.VideoCapture(r"D:\GitHub\Robo_fight\ASRG\video2.mp4")
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    k = 0
    frame_pre = np.zeros((1080, 1920), dtype=np.uint8)
    
    while True:
        start = time.time()
        # frameDict = getFrame(capList)
        # if len(capList) == 1:
        #     joinFrame = frameDict["0"]
        # else:
        #     joinFrame = joinedFrame(frameDict)
        _, joinFrame = cap.read()
        binFrame = cv.cvtColor(joinFrame, cv.COLOR_BGR2GRAY)
        filter_frame = cv.boxFilter(binFrame,  ddepth=-1, dst=binFrame, ksize=(3,3))
        subFrame = cv.absdiff(filter_frame,frame_pre)
        threshFrame = cv.threshold(subFrame,30.0, 255.0, cv.ADAPTIVE_THRESH_MEAN_C, dst=-1)
        contours = cv.findContours(threshFrame[1],cv.RETR_EXTERNAL,cv.CHAIN_APPROX_TC89_L1)
        try:
            cv.drawContours(joinFrame,contours[0],-1,(0,0,255),thickness=5)
        except:
            pass
        frame_pre = filter_frame.copy()
        k +=1 
        if k == 5:
            #cv.imwrite(img=subFrame, filename="./image.jpg")
            k = 0
        cv.imshow("frame", joinFrame)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    # for cap in capList:
    #     cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()