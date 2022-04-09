# https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py

#!/usr/bin/env python
import sys
import os
import time
from pympler.asizeof import asizeof
from serial import Serial, serialutil
import math
import np

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

def send_as_chunks(data):
    size = asizeof(data)
    length = size(data)
    chunk_size = 8 # number of ints
    iterations = int(math.ceil(size / chunk_size))
    print ("Size: " + str(size) + " Length: " + str(length) + " Iterations: " + str(iterations))
    
    for i in range(iterations):
        chunk = []
        if i == iterations - 1:
            chunk = data[i*8: size(data)]
        else:
            chunk = data[i*8: i*8 + 8]
        print (chunk)
        serial.write(chunk)
        # bytesToRead = 0
        # while bytesToRead == 0:
        #     bytesToRead = serial.inWaiting()
        # echo = serial.read(bytesToRead)
        # print(echo)


array_uint8 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], dtype=np.int8)
send_as_chunks(array_uint8)

    