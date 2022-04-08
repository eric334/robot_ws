#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header
from serial import Serial, serialutil
from pympler.asizeof import asizeof
import math
from io import BytesIO

import dynamic_reconfigure.client

class Node:

    def __init__(self):

        camera_topic = "/usb_cam/image_raw/compressed"
        dev = "/dev/ttyACM0"
        baud = "115200"

        self.set_compressedimage_quality(camera_topic, "40")

        rospy.loginfo("Nordic_send - opening serial : " + dev)
        self.serial = Serial(dev, timeout=1, baudrate=baud)

        self.sub_camera = rospy.Subscriber(camera_topic, CompressedImage, self.callback_camera)
        rospy.loginfo("Nordic_send - subscribed to topic : " + camera_topic)
        
        self.sent = False

    def run(self):
        rospy.spin()
    
    # modify headers so they are identifiable on the other end
    def callback_camera(self, compressedImage):
        compressedImage.header.frame_id = "cam"
        self.write_serial(compressedImage)

    def write_serial(self, data):
        self.send_as_chunks(data)
        #return

    def set_compressedimage_quality(self, topic, quality):
            client = dynamic_reconfigure.client.Client(topic, timeout = 3)
            client.update_configuration({ 'format' : 'jpeg', 'jpeg_quality' : int(quality)})

    def send_as_chunks(self, data):
        if self.sent == False:
            
            size = asizeof(data)
            rospy.loginfo("Size: " + str(size))
            chunk_size = 64
            iterations = int(math.ceil(size / chunk_size))
            
            for i in range(iterations):
                chunk = ""
                if i < iterations - 1:
                    chunk = data[i*64: i*64 + 63]
                else:
                    rospy.loginfo("last")
                    chunk = data[i*64: size - i*64]
                rospy.loginfo (chunk)
                self.serial.write(chunk)
                bytesToRead = 0
                while bytesToRead == 0:
                    bytesToRead = self.serial.inWaiting()
                echo = self.serial.read(bytesToRead)
                rospy.loginfo("echo: "+echo)
                if i == 3:
                    break

            self.sent = True

if __name__ == '__main__':
    rospy.init_node('nordic_send', anonymous=True)
    node = Node()
    node.run()

    

