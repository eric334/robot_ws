# https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py

#!/usr/bin/env python
import sys
import os
import time
from pympler.asizeof import asizeof
from serial import Serial, serialutil
import math

dev = '/dev/ttyACM0'
baud = 115200

serial = Serial(dev, timeout=1, baudrate=baud)
serial.close()
serial.open()


# for i in range(10):
#     # string = "test" + str(i)
#     # print("send: " + string)
#     # serial.write("0010".encode())
#     # bytesToRead = 0
#     # while bytesToRead == 0:
#     #     bytesToRead = serial.inWaiting()
#     # data = serial.read(bytesToRead)
#     # print(data)

def send_size_then_data(data):
    data = b''.join([b'0000', bytes(data)])
    size = asizeof(data)

    print ("actual size " + str(size))
    print ("system size " + str(sys.getsizeof(data)))

    if (size > 9999):
        rospy.logerror("fatal error size larger than 9999 bytes")
        return

    size = str(size).zfill(4)

    print("sending " + size)

    serial.write(size.encode())

    bytesToRead = 0
    while bytesToRead == 0:
        bytesToRead = serial.inWaiting()
    echo = serial.read(bytesToRead)
    print("echo " + echo)

    serial.write(data)

def send_as_chunks(data):
    data = bytes(data)
    size = asizeof(data)
    print("Size: " + str(size))
    chunk_size = 64
    iterations = int(math.ceil(size / chunk_size))
    
    for i in range(iterations):
        chunk = data[i*64: i*64 + 63]
        print (chunk)
        serial.write(chunk)
        bytesToRead = 0
        while bytesToRead == 0:
            bytesToRead = serial.inWaiting()
        echo = serial.read(bytesToRead)
        print(echo)




send_as_chunks("the quick brown fox jumped over the lazy dog")

    