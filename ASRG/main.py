import cv2 as cv
from camera_utils import getCap, getFrame
from stitching_frame import getStitchedFrame
from frame_filter import getHsvFrame, getRedFrame, getGreenFrame
from calc_moments import getCentroid
from calc_orientation import getAngle

def main():
    capList = getCap(1)
    while True:
        frameDict = getFrame(capList)
        stitchedFrame = getStitchedFrame(frameDict)

        hsvFrame = getHsvFrame(stitchedFrame)
        redFrame = getRedFrame(hsvFrame)
        greenFrame = getGreenFrame(hsvFrame)
        XY_red = getCentroid(redFrame)
        XY_green = getCentroid(greenFrame)
        angle = getAngle(stitchedFrame,XY_red,XY_green)
        
        cv.imshow("frame", stitchedFrame)

        if cv.waitKey(1) == ord('q'):
            break
    
    for cap in capList:
        cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()