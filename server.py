# Save as server.py 
# Message Receiver
import os
from socket import *

import serial
import time
#import msvcrt


#COMPORT = int(input("Port number: "))
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
#arduino.port = "COM{}".format(COMPORT)
print ("Opening Serial port...")
time.sleep(2)
print (arduino.readline())
time.sleep(2)
print ("Initialization complete")


host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print "Waiting to receive messages..."
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print "Received message: " + data
    (x, y, z, id) = data.split()
    arduino.write('<x'+x[0:7]+'y'+y[0:7]+'z'+z[0:7]+'>')
    print (arduino.readline())
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
