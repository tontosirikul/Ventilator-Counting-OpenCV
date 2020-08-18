import numpy as np
import cv2

VIDEO_PATH = "Images/VDO_Demo.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

while True:
    ret,frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



