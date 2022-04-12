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

        with open("my_file.txt", "wb") as binary_file:
            
            binary_file.write(buffer.getvalue()[:])

        with open("my_file1.txt", "wb") as binary_file:

            # Write bytes to file
            binary_file.write(buffer.getvalue()[:63])

        with open("my_file2.txt", "wb") as binary_file:

            binary_file.write(buffer.getvalue()[63:])

def createVector3(list):
    vector = Vector3()

    vector.x = list[0]
    vector.y = list[1]
    vector.z = list[2]

    return vector


if __name__ == '__main__':
    rospy.init_node('serialize_test', anonymous=True)
    node = Node()
