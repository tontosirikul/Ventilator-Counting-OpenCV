import numpy as np
import cv2
import sys, time, threading

VIDEO_PATH = "eVentilator_VDO_5min.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)