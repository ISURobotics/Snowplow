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
from math import cos
from math import sin
import sys
#import msvcrt


def fixAngle(tol, wpX, wpY, xAct, yAct):
    thetaGood = False
    thetaVehicle = 90
    sensact = 90
    counter = 0
    stateChange = False
    while not thetaGood:
        counter = counter+1
        while arduino.inWaiting():
            readline = arduino.readline()
            sensact = float(readline)
            thetaVehicle = sensact+90
        if(thetaVehicle>=360):
            thetaVehicle = thetaVehicle-360
        #print(sensact)
        thetaDesired = 180/3.1415926535897*math.atan2((wpY-yAct),(wpX-xAct))
        if(thetaDesired<0):
            thetaDesired = 360+thetaDesired
        #we are using act (thetaVehicle) and thetaDesired
        dif = thetaVehicle-thetaDesired
        if(abs(dif)>tol):
            if not stateChange:
                if(dif>0 and dif<=180):
                    turnStr = 'r'
                    arduino.write('r')
                    stateChange = True
                elif (dif>180):
                    arduino.write('l')
                    stateChange = True
                    turnStr = 'l'
                elif(dif<=0 and dif>=-180):
                    arduino.write('l')
                    stateChange = True
                    turnStr = 'l'
                elif(dif<-180):
                    arduino.write('r')
                    stateChange = True
                    turnStr = 'r'
                else:
                    arduino.write('s')
                    print("No angle criterion matched...")
            if(counter%10==0):
                print(turnStr)
                print('thetaVehicle: ' + str(thetaVehicle)+' thetaDesired: ')+str(thetaDesired)+' dif: ' + str(dif)
        else:
            print('theta is good!')
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
waypoints = [[0,3],[0,7],[0,10], [0,5]]
#waypoints = [[3,3],[0,-2],[0,4]]

host = ""
port = 13000
buf = 1024
addr = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8089))
s.listen(5)
orientationTol = 15
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
        #x,y,z,ID = getPose()
#This chunk of code corrects the marker location to the center of the "marker cube"
#Assumes marker one is on the back of the plow, with three facing forward. If it was a compass, NWSE would be 3412.
        while arduino.inWaiting():
            anglestr = arduino.readline()
            ts = float(anglestr) #theta sensor in degrees
            act = ts+90 #plow angle in degrees (90 is straight up field)
        if act>=360:
            act = act-360
        x = x+cos(ts+offset*(ID-1))*12/39.4
        y = y+sin(ts+offset*(ID-1))*12/39.4
#This calculates distance to the waypoint and sets the distance tolerance
        distToWP = sqrt(pow((wpY-y),2)+pow((wpX-x),2)) #meters
        distTol = .75 #in meters        
        print("(X,Y): ("+str(x)+","+str(y)+"). Desired: ("+str(wpX)+","+str(wpY)+").    Orientation: " +str(act))

#This is navigation control:
        if(distToWP>distTol): #If we're too far away from the wapoint
            headingCorrect = fixAngle(orientationTol, wpX, wpY, x, y)#fix angle is able to fix the angle without relying on a positional update.  Should make it work a bit better!
            if(headingCorrect): #If heading is correct, drive towards the waypoint.
                print("Drive forward")
                arduino.write('f')
                time.sleep(.25)
        else:   #If we're close enough, stop for two seconds. 
            arduino.write('s')
            print('waypoint reached!')
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


