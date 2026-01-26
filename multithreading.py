import cv2
import threading
import time

num_camers = 2

def get_frame(id,frames,locks,stop_flag):
    cap = cv2.VideoCapture(id)

    if not cap.isOpened():
        return
    
    while not stop_flag.is_set():
        start = time.time()
        _, frame = cap.read()
        cv2.imshow(f"frame{id}",frame)
        print(f"{time.time() - start:.4f}", f"frame{id}")

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

def main():
    frames = {}
    locks = {}
    camera_thread = []
    stop_flag = threading.Event()
    for i in range(num_camers):
        frames[i] = None
        locks[i] = threading.Lock()

        thread = threading.Thread(target=get_frame, 
                                    args=(i,frames,locks,stop_flag),
                                    daemon=True)
        thread.start()
        camera_thread.append(thread)
    time.sleep(2)

    while not stop_flag.is_set():
        pass

if __name__ == "__main__":
    main()