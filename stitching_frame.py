import cv2

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

while True:
    _ ,frame1 = cap1.read()
    _ ,frame2 = cap2.read()

    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    status, stitched_frame = stitcher.stitch([frame1,frame2])
    # cv2.imshow("frame1", frame1)
    # cv2.imshow("frame2", frame2)

    if status == cv2.Stitcher_OK:
        cv2.imshow("stitched frame",stitched_frame)
    else:
        print("Ошибка", status)

    if cv2.waitKey(1) == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()