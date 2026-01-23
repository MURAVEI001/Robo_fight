import cv2
import numpy as np

def nothing(x):
    pass

image = cv2.namedWindow("image")

cv2.createTrackbar("H_min","image",0,255,nothing)
cv2.createTrackbar("S_min","image",0,255,nothing)
cv2.createTrackbar("V_min","image",0,255,nothing)
cv2.createTrackbar("H_max","image",0,255,nothing)
cv2.createTrackbar("S_max","image",0,255,nothing)
cv2.createTrackbar("V_max","image",0,255,nothing)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    h_low = cv2.getTrackbarPos("H_min","image")
    s_low = cv2.getTrackbarPos("S_min","image")
    v_low = cv2.getTrackbarPos("V_min","image")
    h_up = cv2.getTrackbarPos("H_max","image")
    s_up = cv2.getTrackbarPos("S_max","image")
    v_up = cv2.getTrackbarPos("V_max","image")
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(hsv_frame, np.array([h_low,s_low,v_low]), np.array([h_up,s_up,v_up]))
    frame = cv2.bitwise_and(frame,frame,mask=mask)
    
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()