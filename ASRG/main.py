import cv2 as cv
import time
from camera_utils import getCap, getFrame
from stitching_frame import joinedFrame

def main():
    # capList = getCap(2)
    cap = cv.VideoCapture(r"ASRG/video2.mp4")
    backSub = cv.createBackgroundSubtractorKNN()
    while True:
        start = time.time()
        # frameDict = getFrame(capList)  
        # joinFrame = joinedFrame(frameDict)
        _, frame = cap.read()        
        bin_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

        figMsk = backSub.apply(bin_frame)
        contours, hierarchy = cv.findContours(figMsk, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        frame_ct = cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
        retval, mask_thresh = cv.threshold( figMsk, 180, 255, cv.THRESH_BINARY)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        mask_eroded = cv.morphologyEx(mask_thresh, cv.MORPH_OPEN, kernel)
        min_contour_area = 800  # Define your minimum area threshold
        large_contours = [cnt for cnt in contours if cv.contourArea(cnt) > min_contour_area]
        frame_out = frame.copy()
        for cnt in large_contours:
            x, y, w, h = cv.boundingRect(cnt)
            frame_out = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 3)
        
        # отображаем результат
        cv.imshow('Frame_final', frame_out)
        print(f"{time.time() - start:.4f}")

        if cv.waitKey(30) == ord('q'):
            break
    
    # for cap in capList:
    #     cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()