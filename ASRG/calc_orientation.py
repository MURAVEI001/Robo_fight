import cv2 as cv
import math

def getAngle(frame,red_xy,green_xy):
    if red_xy and green_xy:
        cv.line(frame, (red_xy[0],0),(red_xy[0],480), (128,128,255),5)
        cv.line(frame, (0,red_xy[1]),(len(frame[0]),red_xy[1]), (128,128,255),5)
        cv.line(frame, (green_xy[0],green_xy[1]),(green_xy[0],green_xy[1]), (128,255,128),10)

        opposite_catheter = red_xy[0] - green_xy[0]
        adjacent_catheter = red_xy[1] - green_xy[1]

        angle = math.degrees(math.atan2(opposite_catheter,adjacent_catheter))
        cv.putText(frame, f"{angle}",(red_xy[0]-30,red_xy[1]-30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
        return angle