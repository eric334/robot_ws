# https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py

#!/usr/bin/env python
import sys
import os
import time
from pympler.asizeof import asizeof
from serial import Serial, serialutil

dev = '/dev/ttyACM0'
baud = 115200

serial = Serial(dev, timeout=1, baudrate=baud)
serial.close()
serial.open()

for i in range(10):
    string = "test" + str(i)
    print("send: " + string)
    serial.write("0010".encode())
    bytesToRead = 0
    while bytesToRead == 0:
        bytesToRead = serial.inWaiting()
    data = serial.read(bytesToRead)
    print(data)

def send_size_then_data(data):
    size = asizeof(data)

    if (size > 9999):
        rospy.logerror("fatal error size larger than 9999 bytes")
        return

    size = str(size).zfill(4)

    serial.write(size.encode())

    bytesToRead = 0
    while bytesToRead == 0:
        bytesToRead = serial.inWaiting()
    data = serial.read(bytesToRead)

    if data == "1":
        serial.write(data)
    else:
        rospy.logerror("fatal error did not recieve reply")
        return

    

    