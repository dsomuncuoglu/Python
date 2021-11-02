import cv2
import numpy as np
import pyautogui

face_cascade=cv2.CascadeClassifier('cascade.xml')

capture=cv2.VideoCapture(0)

prev_y=0

while True:
    ret,frame=capture.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.1,4)


    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if y < prev_y :
            pyautogui.moveTo(300, 350)

        prev_y=y

    cv2.imshow('frame',frame)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break

capture.release()
cv2.destroyAllWindows()