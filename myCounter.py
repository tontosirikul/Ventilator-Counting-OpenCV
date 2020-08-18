import numpy as np
import cv2
import sys, time, threading
from datetime import datetime
import csv

VIDEO_PATH = "eVentilator_VDO_5min.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

lower_blue = np.array([88,80,120])
upper_blue = np.array([103,254,255])

kernel = np.ones((15,15),np.uint8)
count = 0
compress = False
bpm = 0
t = time.process_time()
darea = 0
tdarea = 0

area_max = 390000
run = True

row_list = []


def getContourDraw(img,mask):
    _, contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        area = w * h
        if area > 5000:
         cv2.drawContours(img, contours, -1,(0,255,0),2)
         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 5)
    return img,area,contours,h

def process(img):
    image = img.copy()
    blur_image = cv2.GaussianBlur(img,(5,5),0)
    hsv = cv2.cvtColor(blur_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    #close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening,kernel,iterations = 1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    frame,area,contour,h = getContourDraw(image,erosion)
    return frame,area,contour,h

def draw_text_on_image(img_draw, count,bpm,darea):
    # cv2.rectangle(img_draw, (0, 10), (500, 40), (0,0,0), -1)
    cv2.putText(img_draw,'pressed count: ' + str(round(count)), 
        (10,20),                  # bottomLeftCornerOfText
        cv2.FONT_HERSHEY_SIMPLEX, # font 
        0.5,                      # fontScale
        (0,255,255),            # fontColor
        2)                        # lineType
    
    cv2.putText(img_draw,'BPM: ' + str(round(bpm)), 
        (10,40),                  # bottomLeftCornerOfText
        cv2.FONT_HERSHEY_SIMPLEX, # font 
        0.5,                      # fontScale
        (0,255,255),            # fontColor
        2) 

    cv2.putText(img_draw,'area changed %: ' + str(round(darea*100)), 
        (10,60),                  # bottomLeftCornerOfText
        cv2.FONT_HERSHEY_SIMPLEX, # font 
        0.5,                      # fontScale
        (0,255,255),            # fontColor
        2) 
    return img_draw


while True:
    ret,frame = cap.read()
    if ret == True:
        frame,area,contour,h = process(frame)
        #print(str(area_max)+' '+str(area)+' '+str(area_max-area))
        darea = area_max-area
        if compress == False:
            if  h <= 399 and h >= 300:
                compress = True
                #print("down")
            elif h > 400:
                #print("uppp")
                compress == False
        if compress == True:
            if h <= 399 and h >= 300:
                #print("down")
                compress == True
            elif h > 400:
                #print("Upp")
                compress = False
                count = count + 1
                bpm = count*60/(time.process_time()-t)
                dateTimeObj = datetime.now()
                tdarea = darea/area_max
                list = [count,bpm,tdarea]
                row_list.append(list)

                with open('bpm.csv', mode='a', newline='') as csv_file:
                    writer = csv.writer(csv_file,quoting=csv.QUOTE_NONNUMERIC, delimiter='|')
                    writer.writerow(row_list) 

                row_list.clear()

        frame = draw_text_on_image(frame,count,bpm,tdarea)
        cv2.imshow('frame1',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            run = False
            break
    else:
        run = False
        break

# with open('ventilator.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['COUNT','BPM','DATE/TIME'])
#             writer.writerow(row_list)
# state_thread.stop()
cap.release()
cv2.destroyAllWindows()

