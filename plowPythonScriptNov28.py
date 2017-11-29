# Save as server.py 
# Message Receiver
import os
from socket import *
import socket
import serial
import time
from time import sleep
#import matplotlib
import math
from math import sqrt
import sys
#import msvcrt

def fixAngle(tol, wpX, wpY, xAct, yAct):
    thetaGood = False
    while not thetaGood:
        while arduino.inWaiting():
            readline = arduino.readline()
            sensact = float(readline)
            act = sensact+90
        if(act>=360):
            act = act-360
        thetaDesired = 180/3.14159*math.atan2((wpY-yAct),(wpX-xAct))
        thetaSensDes = thetaDesired-90
        if(thetaSensDes<0):
            thetaSensDes=360+thetaSensDes
        dif = thetaSensDes-sensact
        if(abs(dif)<tol):
            thetaGood = True
            break
        if((abs(dif))<180 and dif>0):
            arduino.write('l') #print("Turn Counterclockwise (left)")
        elif(abs(dif)<180 and dif <0):
            arduino.write('r') #print("Turn clockwise (right)")
        elif(abs(dif)>180 and dif>0):
            arduino.write('r')#print("Turn clockwise (right case 2)")
        else:
            arduino.write('l')#print("Turn left (case 2)")
    return True
			
		
	

#COMPORT = int(input("Port number: "))
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
#arduino.port = "COM{}".format(COMPORT)
print ("Opening Serial port...")
time.sleep(2)
print (arduino.readline())
time.sleep(2)
print ("Initialization complete")

#waypoints = [[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,13],[0,12],[0,11],[0,10],[0,9],[0,8],[0,7],[0,6],[0,5],[0,4],[0,3]]
#waypoints =[[0,3],[1,4],[1,5],[0,6],[-1,5],[0,3]]
waypoints = [[0,3],[0,8],[0,4]]

host = ""
port = 13000
buf = 1024
addr = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8089))
s.listen(5)
orientationTol = 10
orientation = 100
myByte = 0
offset = 3.14159/2

print "Waiting to receive messages..."
for waypoint in waypoints:
    wpY = waypoint[1]
    wpX = waypoint[0]
    while True:
#this chunk of code gets the location of the marker
        connection, address = s.accept()
        data = connection.recv(128)
        (xstr, zstr, ystr, IDstr) = data.split() #note that our field coordinates are (x,y).
        x = float(xstr)/39.4
        y = float(ystr)/39.4
        z = float(zstr)/39.4
        ID = int(IDstr)
#This chunk of code corrects the marker location to the center of the "marker cube"
#Assumes marker one is on the back of the plow, with three facing forward. If it was a compass, NWSE would be 3412.
        while arduino.inWaiting():
            anglestr = arduino.readline()
            ts = float(anglestr) #theta sensor in degrees
            act = sensact+90 #plow angle in degrees (90 is straight up field)
        x = x+cos(ts+offset*(ID-1))
        y = y+sin(ts+offset*(ID-1))
#This calculates distance to the waypoint and sets the distance tolerance
        distToWP = sqrt(pow((wpY-y),2)+pow((wpX-x),2)) #meters
        distTol = .75 #in meters        
        print("(X,Y): ("+str(x)+","+str(y)+"). Desired: ("+str(wpX)+","+str(wpY)+").    Orientation: " +str(ts+90))

#This is navigation control:
        if(distToWP>distTol): #If we're too far away from the wapoint
            headingCorrect = fixAngle(orientationTol, wpX, wpY, x, y)#fix angle is able to fix the angle without relying on a positional update.  Should make it work a bit better!
            if(headingCorrect): #If heading is correct, drive towards the waypoint.
                arduino.write('f')
        else:   #If we're close enough, stop for two seconds. 
            arduino.write('s')
            time.sleep(2)
            break

    print('next wp')
UDPSock.close()
os._exit(0)


#point in right direction
#if within right direction tolerance
#go in a straight line towards next waypoint until
#distance < tolerance
#go to next iteration of the for loop, or the next waypoint
#if done, stop


