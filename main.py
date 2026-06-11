import cv2 as cv
import numpy as np
import time
import math
import socket
import struct
from ip import now_ip

HOST = now_ip() #local host
PORT = 3333 #port number

# 0 50 120 255 255 206 - label
# 180 0 0 255 255 255 - red
# 0 0 0 50 255 255 - red
# 50 0 0 120 255 255 - green

def filter_hsv(frame):
    filter = np.array([[0,50,120],[255,255,206]])
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV_FULL)
    mask = cv.inRange(hsv_frame, filter[0], filter[1])
    return cv.bitwise_or(frame,frame, mask=mask)

def filter_red(frame):
    frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV_FULL)
    red = np.array([[[180,1,1],[255,255,255]],[[0,1,1],[40,255,255]]])
    mask1 = cv.inRange(frame,red[0][0],red[0][1])
    mask2 = cv.inRange(frame,red[1][0],red[1][1])
    red_mask = cv.bitwise_or(mask1,mask2)
    return red_mask

def filter_green(frame):
    frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV_FULL)
    green = np.array([[50,0,0],[120,255,255]])
    green_mask = cv.inRange(frame,green[0],green[1])
    return green_mask

def calc_centroid(frame):
    moments = cv.moments(frame,binaryImage=True)

    if moments["m00"]==0:
        return (0,0)
    else:
        x = moments["m10"]//moments["m00"]  
        y = moments["m01"]//moments["m00"]
        xy = (int(x),int(y))
        return xy

def calc_orientation(frame,red,green):
    if red and green:
        cv.line(frame, (red[0],0),(red[0],480), (128,128,255),5)
        cv.line(frame, (0,red[1]),(len(frame[0]),red[1]), (128,128,255),5)
        cv.line(frame, (green[0],green[1]),(green[0],green[1]), (128,255,128),10)

        opposite_catheter = red[0] - green[0]
        adjacent_catheter = red[1] - green[1]

        angle = math.degrees(math.atan2(opposite_catheter,adjacent_catheter))
        cv.putText(frame, f"{angle}",(red[0]-30,red[1]-30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
        return angle

def stitching(frames):
    return np.concatenate([frames[f"{i}"] for i in range(len(frames))], axis=1)

def init_camers(num_camers):
    caps = []
    for i in range(num_camers):
        caps.append(cv.VideoCapture(i))
    return caps

def send_data(HOST, PORT):
    print("TCP Server is running...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Socket created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT)) #привязка сокета к адресу и порту
        print("Socket bind complete")
        s.listen() #прослушивание входящих подключений
        print("Socket is listening")
        conn, addr = s.accept() #принятие входящего подключения
        return conn, addr
            
def main():
    caps = init_camers(1)
    frames = {}
    #conn, addr = send_data(HOST,PORT)
    # print('Connected by', addr)
    while True:
        start = time.time()
        for i, cap in enumerate(caps):
            _, frames[f"{i}"] = cap.read()

        # frame = stitching(frames)
        # filter_frame = filter_hsv(frame)
        # red_frame = filter_red(filter_frame)
        # green_frame = filter_green(filter_frame)
        # red_xy = calc_centroid(red_frame)
        # green_xy = calc_centroid(green_frame)
        # angle = calc_orientation(frame,red_xy,green_xy)

        # data = struct.pack('5f', red_xy[0], red_xy[1], angle, 0, 0)  #упаковка данных в байты
        #conn.send(data) #отправка данных клиенту
        
        # cv2.imshow("filter_frame", filter_frame)
        # cv2.imshow("red_frame", red_frame)
        # cv2.imshow("green_frame", green_frame)
        
        for i in range(len(frames)):
            cv.imshow(f"frame_{i}", frames[f"{i}"])

        print(f"{time.time() - start:.4f}")

        if cv.waitKey(1) == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()