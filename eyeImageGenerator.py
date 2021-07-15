import numpy as np
import cv2
import os
import time

right_eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_righteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_lefteye_2splits.xml')
# make directory for the concerned type
print("Enter the name")
dir_name = input()
directory = dir_name
parent_dir = "images"
path = os.path.join(parent_dir, directory) 
os.mkdir(path)

cap = cv2.VideoCapture(0)
t_end = time.time() + 10
img_count = 1
while time.time() < t_end:
    ret, frame = cap.read()
    height,width = frame.shape[:2] 
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    left_eye = left_eye_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    right_eye = right_eye_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    for (x, y, w, h) in right_eye:
        roi_gray = gray[y:y+h, x:x+w]
        
        color = (0, 255, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h

        img_item = 'images/{}/{}{}.png'.format(directory,directory,img_count)
        cv2.imwrite(img_item, roi_gray)
        img_count += 1
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
    for (x, y, w, h) in left_eye:
        roi_gray = gray[y:y+h, x:x+w]
        
        color = (0, 255, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h

        img_item = 'images/{}/{}{}.png'.format(directory,directory,img_count)
        cv2.imwrite(img_item, roi_gray)
        img_count += 1
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()