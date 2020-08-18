import numpy as np
import cv2
import sys, time, threading

VIDEO_PATH = "Images/VDO_Demo.mp4"
capturing_flag = True
counter = 0

cap = cv2.VideoCapture(VIDEO_PATH)

def thread1_routine():
    while True:
        print("Test %d" % counter)
        time.sleep(1)

thread1 = threading.Thread(target=thread1_routine)
thread1.start()



while True:
    ret,frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord(''):
        break
    counter += 1
cap.release()
cv2.destroyAllWindows()


# def showImage():
#     while capturing_flag:
#         ret,frame = cap.read()
        # print(frame)
        # cv2.imshow('frame', frame)
    # cap.release()
    # cv2.destroyAllWindows()
# im_process_thread = threading.Thread(target=showImage)
# im_process_thread.start()

# if input("Exit?"):
#     capturing_flag = False
    # im_proess_thread.stop()




