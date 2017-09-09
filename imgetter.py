import numpy as np
import cv2
import glob
import yaml
from cv2 import aruco
import os
import sys
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1280,720)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1280,720))
time.sleep(0.1)

mystring = 'checkerboardcals'
i = 0

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    
    time.sleep(1)
    image = frame.array
    tempstring = mystring + str(i) + '.jpg'
    print(tempstring)
    cv2.imshow('im',image)
    cv2.waitKey(250)
    cv2.imwrite(tempstring,image)
    rawCapture.truncate(0)
    i += 1
    if i==50:
        break
