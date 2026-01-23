import cv2
import numpy as np
import time

# 0 50 120 255 255 206 - label
# 180 0 0 255 255 255 - red
# 0 0 0 50 255 255 - red
# 50 0 0 120 255 255 - green

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

def filter_red(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV_FULL)
    red = np.array([[[180,1,1],[255,255,255]],[[0,1,1],[40,255,255]]])
    mask1 = cv2.inRange(frame,red[0][0],red[0][1])
    mask2 = cv2.inRange(frame,red[1][0],red[1][1])
    red_mask = cv2.bitwise_or(mask1,mask2)
    return red_mask

def filter_green(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV_FULL)
    green = np.array([[50,0,0],[120,255,255]])
    green_mask = cv2.inRange(frame,green[0],green[1])
    return green_mask

def calc_centroid(frame):
    moments = cv2.moments(frame,binaryImage=True)

    # заменить на обработку что метка потеряна
    if moments["m00"]==0:
        x = len(frame[0])//2
        y = len(frame)//2
    else:
        x = moments["m10"]//moments["m00"]
        y = moments["m01"]//moments["m00"]
    
    xy = (int(x),int(y))
    return xy

def calc_orientation(frame,red,green):
    cv2.line(frame, (red[0],0),(red[0],480), (128,128,255),5)
    cv2.line(frame, (0,red[1]),(640,red[1]), (128,128,255),5)
    cv2.line(frame, (green[0],green[1]),(green[0],green[1]), (128,255,128),10)

    if green[0] >= red [0] and green[1] >= red[1]:
        print("^")
        print("|")
    
    elif green[0] >= red [0] and green[1] <= red[1]:
        print("<----")
    
    elif green[0] <= red [0] and green[1] >= red[1]:
        print("---->")
    
    elif green[0] <= red [0] and green[1] <= red[1]:
        print("|")
        print("v")

while True:
    start = time.time()
    ret, frame = cap.read()

    filter = np.array([[0,50,120],[255,255,206]])
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(hsv_frame, filter[0], filter[1])
    filter_frame = cv2.bitwise_or(frame,frame, mask=mask)

    red_frame = filter_red(filter_frame)
    green_frame = filter_green(filter_frame)
    red_xy = calc_centroid(red_frame)
    green_xy = calc_centroid(green_frame)

    calc_orientation(frame,red_xy,green_xy)

    # cv2.imshow("filter_frame", filter_frame)
    # cv2.imshow("red_frame", red_frame)
    # cv2.imshow("green_frame", green_frame)
    # cv2.imshow("frame", frame)

    print(f"{time.time() - start:.10f}")

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()