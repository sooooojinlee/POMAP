import sys

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2
import numpy as np

from os import listdir
from os.path import isfile, join


cap = cv2.VideoCapture('http://192.168.0.37:8090/?action=stream')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # 프레임 폭 320으로 지정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # 프레임 높이 240으로 지정

count = 0 

if cap.isOpened():
    while True:
        ret, img = cap.read()

        if ret:
            cv2.imshow('camera', img)
            cv2.imwrite("./images/frame%d.jpg" % count, img)
            
            count+=1

            if cv2.waitKey(1) == 27: 
                break
        else:
            print('no frame!')
else:
    print("can't open video")
cap.release()
cv2.destroyAllWindows()
    