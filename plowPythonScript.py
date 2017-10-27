# Save as server.py 
# Message Receiver
import os
from socket import *

import serial
import time
from time import sleep
#import matplotlib
import math
from math import sqrt
import sys
#import msvcrt


#COMPORT = int(input("Port number: "))
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
#arduino.port = "COM{}".format(COMPORT)
print ("Opening Serial port...")
time.sleep(2)
print (arduino.readline())
time.sleep(2)
print ("Initialization complete")

waypoints = [[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,13],[0,12],[0,11],[0,10],[0,9],[0,8],[0,7],[0,6],[0,5],[0,4],[0,3]]


host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
orientationTol = 10
myByte = 0
print "Waiting to receive messages..."
for waypoint in waypoints:
    wpY = waypoint[1]
    wpX = waypoint[0]
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        print "Received message: " + data
        (xstr, zstr, ystr, id) = data.split() #note that our field coordinates are (x,y).
        x = float(xstr)
        y = float(ystr)
        z = float(zstr)
        readline = arduino.readline()
        print(readline)
        if(readline!='\r\n'):
            readline = readline[:-2]
            if(readline==''):
                readline = '0'
            orientation = math.degrees(float(readline))
        else:
            orientation = 0
        print('calculating direction')
        desiredHeading = math.atan2(wpY-y,wpX-x)
        distToWP = sqrt(pow((wpY-y),2)+pow((wpX-x),2))
        distTol = .2
        speed = 0x4
        
        if(desiredHeading>=0): #turn left
            directionMR = 1 #forward
            directionML = 0 #back
        else:
            directionML = 1 #turn right
            directionMR = 0
        if(abs(desiredHeading-orientation)<orientationTol): #if within direction tolerance
            headingCorrect = True #say we're good to drive forward
        else:
            headingCorrect = False
        if headingCorrect:
            if(distToWP>distTol):
                directionMR = 1
                directionML = 1
            else:
                break
        myByte = myByte|speed
        if(directionMR == 1):
            myByte = myByte | 0b00010000
        else:
            myByte = myByte & 0b11101111
        if(directionML == 1):
            myByte = myByte | 0b00100000
        else:
            myByte = myByte & 0b11011111
        arduino.write('\x7F')
        sleep(.05)
        sys.stdout.flush()
    
    print('next wp')
UDPSock.close()
os._exit(0)


#point in right direction
#if within right direction tolerance
#go in a straight line towards next waypoint until
#distance < tolerance
#go to next iteration of the for loop, or the next waypoint
#if done, stop


