#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import socket
import sys
import numpy as np
import serial

def buffered_readLine(socket):
    line = ""
    while True:
        part = socket.recv(1)
        if not part:
            return None
        if part != "\n":
            line+=part
        elif part == "\n":
            break
    return line

arduino = serial.Serial('/dev/ttyACM0',9600)
keep_running = True
name = "10.27.173.205"
port = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket created'
try:
    sock.bind((name, port))
except socket.error as err:
    print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
    sys.exit()

print 'Socket Bind Success!'
sock.listen(10)
conn, addr = sock.accept()
print('socket accepted')


#thresh low = 218 (5 ft), 250 is long range something
closeVal = 218
farVal = 250





def display_depth(dev, data, timestamp):
    global keep_running
    global conn
    global addr
    buf = buffered_readLine(conn);
    #if not buf:
     #   conn, addr = sock.accept()
      #  return
    #print buf
    auto = int(float(buf))
    shifted = int(buf) >> 7
    # print("auto: " + str(auto))
    # print(" buf: " +str(buf))
    # print(" shifted: " + str(shifted))
    depthimg = frame_convert2.pretty_depth_cv(data)
    eroded = cv2.erode(depthimg,(7,7), iterations = 3) #filter the image
    dilated = cv2.dilate(eroded,(7,7),iterations = 3)  #filter the image more
    #cv2.rectangle(dilated, (280, 200), (360, 280), (0), 3) #draw rectangle in the center for analysis
    roi = dilated[200:280,280:360] #actual pixels to be analyzed for the mean
    mask = cv2.inRange(dilated, closeVal, farVal)
    topHalf = mask[0:240,0:640]
    #cv2.imshow('Depth', topHalf)
    contours = cv2.findContours(topHalf.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    centerX = 320
    if (shifted == 1):
        if len(contours)>0:
            humanCnt = max(contours, key=cv2.contourArea) #pick the biggest shape
            x,y,w,h = cv2.boundingRect(humanCnt)
            centerX = (x+x+w)/2
            #print(centerX)
            cv2.rectangle(topHalf,(x,y),(x+w,y+h),125,2)
            meanValue = roi.mean()
            depthft = meanValue*meanValue*.000892-.292*meanValue+26.5
            #print(depthft)
            if(depthft<6): #stop
                # arduino.write(0x00)
                arduino.write('\x00')
            elif(centerX<300): #left
                # arduino.write(0x4D)
                arduino.write('\x4D')
            elif(centerX>340):#right
                # arduino.write(0x1D)
                arduino.write('\x1D')
            else: #forward
                # arduino.write(0x2D)
                arduino.write('\x2D')
        else: #stop
            # arduino.write(0x00)
            arduino.write('\x00')
    else:
        arduino.write(chr(int(buf)))
    cv2.imshow('Mask',topHalf)
    if cv2.waitKey(10) == 27:
        keep_running = False
        print dilated.shape
        print dilated.dtype
        arduino.write('\x00')
        sock.close()


def display_rgb(dev, data, timestamp):
    global keep_running
    #cv2.imshow('RGB', frame_convert2.video_cv(data))
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill


print('Press ESC in window to stop')
freenect.runloop(depth=display_depth,
                 video=display_rgb,
                 body=body)
