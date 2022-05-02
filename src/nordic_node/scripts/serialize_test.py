#!/usr/bin/env python
import sys
import os
import time
from serial import Serial, serialutil
import rospy
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import CompressedImage
from io import BytesIO
from pympler.asizeof import asizeof
import pickle
import math

class Node:
    def __init__(self):

        obj = TwistStamped()
        obj.twist.linear = createVector3([.3,.1,0])
        obj.twist.angular = createVector3([.2,0,.1])
        obj.header.frame_id = ";akldsjf;alksjfd;lkadja;lksjdf;alkjdf;klaj;dflkaj;slkfdja;lsdfkj;asd"

        print(obj)

        print(asizeof(obj))

        buffer = BytesIO()
        obj.serialize(buffer)

        # getvalue on python 2.7 , getbuffer on python 3
        print(buffer.getvalue())

        print(len(buffer.getvalue()))

        dev = "/dev/ttyACM0"
        baud = "115200"

        self.serial = Serial(dev, timeout=1, baudrate=baud)

        self.send_as_chunks(buffer.getvalue())
    
    def send_as_chunks(self, data):
        data = bytes(data)
        size = asizeof(data)
        print("Size: " + str(size))
        chunk_size = 64
        iterations = int(math.ceil(size / chunk_size))
        
        for i in range(iterations):
            chunk = []
            if i == iterations - 1:
                chunk = data[i*8: size(data)]
            else:
            chunk = data[i*8: i*8 + 8]
            print (chunk)
            self.serial.write(chunk)

def createVector3(list):
    vector = Vector3()

    vector.x = list[0]
    vector.y = list[1]
    vector.z = list[2]

    return vector


if __name__ == '__main__':
    rospy.init_node('serialize_test', anonymous=True)
    node = Node()
