import cv2 as cv
import time
from camera_utils import getCap, getFrame
from stitching_frame import getStitchedFrame
from detect_label import detectLabelBlack
from frame_filter import getHsvFrame, getRedFrame, getGreenFrame
from calc_moments import getCentroid
from calc_orientation import getAngle
from server_utils import getIp,initServer,sendData

def main():
    ipHost = getIp()
    port = 3333
    #conn = initServer(ipHost,port)
    capList = getCap(1)
    prev_time = time.time()
    frame_count = 0
    while True:
        frameDict = getFrame(capList)            

        stitchedFrame = getStitchedFrame(frameDict)
        croppedFrame = detectLabelBlack(stitchedFrame)

        hsvFrame = getHsvFrame(croppedFrame)
        redFrame = getRedFrame(hsvFrame)
        greenFrame = getGreenFrame(hsvFrame)
        XY_red = getCentroid(redFrame)
        XY_green = getCentroid(greenFrame)
        angle = getAngle(croppedFrame,XY_red,XY_green)
        #print(f"{time.time() - start:.4}f"{time.time() - start:.4}")
        #sendData(conn, XY_red[0], XY_red[1], angle, 0, 0)
        cv.imshow("frame", croppedFrame)

        frame_count += 1
        
        curr_time = time.time()
        if curr_time - prev_time >= 1.0:
            fps = frame_count / (curr_time - prev_time)
            print(f"FPS: {fps:.2f}")
        
            frame_count = 0
            prev_time = curr_time

        if cv.waitKey(1) == ord('q'):
            break
    
    for cap in capList:
        cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()