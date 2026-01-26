
def main():

    import cv2
    import numpy as np
    import time

    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        start = time.time()
        _ ,frame1 = cap1.read()
        _ ,frame2 = cap2.read()

        image = np.concatenate([frame1,frame2], axis=1)
        cv2.imshow("image",image)
        print(f"{time.time() - start:.10f}")
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()