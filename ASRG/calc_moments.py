import cv2 as cv

def getCentroid(frame):
    moments = cv.moments(frame,binaryImage=True)

    if moments["m00"]==0:
        return (0,0)
    else:
        x = moments["m10"]//moments["m00"]  
        y = moments["m01"]//moments["m00"]
        xy = (int(x),int(y))
        return xy