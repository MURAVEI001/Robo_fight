import cv2
import numpy as np
import time
import math

# 0 50 120 255 255 206 - label
# 180 0 0 255 255 255 - red
# 0 0 0 50 255 255 - red
# 50 0 0 120 255 255 - green

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

    if moments["m00"]==0:
        return None
    else:
        x = moments["m10"]//moments["m00"]
        y = moments["m01"]//moments["m00"]
        xy = (int(x),int(y))
        return xy

def calc_orientation(frame,red,green):
    if red and green:
        cv2.line(frame, (red[0],0),(red[0],480), (128,128,255),5)
        cv2.line(frame, (0,red[1]),(len(frame[0]),red[1]), (128,128,255),5)
        cv2.line(frame, (green[0],green[1]),(green[0],green[1]), (128,255,128),10)

        opposite_catheter = red[0] - green[0]
        adjacent_catheter = red[1] - green[1]

        angle = math.degrees(math.atan2(opposite_catheter,adjacent_catheter))
        cv2.putText(frame, f"{angle}",(red[0]-30,red[1]-30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))

def stitching(frames):
    return np.concatenate([frames[f"{i}"] for i in range(len(frames))], axis=1)

def init_camers(num_camers):
    caps = []
    for i in range(num_camers):
        caps.append(cv2.VideoCapture(i, cv2.CAP_DSHOW))
        caps[i].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        caps[i].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return caps

def main():
    caps = init_camers(1)
    frames = {}
    while True:
        start = time.time()
        for i, cap in enumerate(caps):
            _, frames[f"{i}"] = cap.read()

        frame = stitching(frames)
        # cv2.imwrite("frame.jpg",frame)
        # input()

        filter = np.array([[0,50,120],[255,255,206]])

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        mask = cv2.inRange(hsv_frame, filter[0], filter[1])
        filter_frame = cv2.bitwise_or(frame,frame, mask=mask)

        red_frame = filter_red(filter_frame)
        green_frame = filter_green(filter_frame)
        red_xy = calc_centroid(red_frame)
        green_xy = calc_centroid(green_frame)

        calc_orientation(frame,red_xy,green_xy)

        cv2.imshow("filter_frame", filter_frame)
        cv2.imshow("red_frame", red_frame)
        cv2.imshow("green_frame", green_frame)
        cv2.imshow("frame", frame)

        print(f"{time.time() - start:.4f}")

        if cv2.waitKey(1) == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()