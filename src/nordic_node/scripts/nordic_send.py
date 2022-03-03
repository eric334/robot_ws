#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import CompressedImage
from serial import Serial, serialutil

import dynamic_reconfigure.client

camera_topic = rospy.get_param("~camera_topic", "usb_cam/image_raw/compressed")
hector_topic = rospy.get_param("~hector_topic", "TODO")
jpeg_quality = rospy.get_param("~jpeg_quality_level", "50")

class Node:

    def __init__(self):
        global camera_topic
        global hector_topic

        dev = rospy.get_param("~dev", "/dev/ttyACM0")
        baud = int(rospy.get_param("~baud", "115200"))
        
        self.serial = Serial(dev, timeout=1, baudrate=baud)

        self.sub_camera = rospy.Subscriber(camera_topic, CompressedImage, self.callback)
        self.sub_hector = rospy.Subscriber(hector_topic, CompressedImage, self.callback)

    def run(self):
        rospy.spin()

    def callback(self, data):
        self.serial.write(data)



def set_compressedimage_quality(topic):
        client = dynamic_reconfigure.client.Client(topic, timeout = 3)
        parameters = client.get_configuration()
        params = { 'format' : 'jpeg', 'jpeg_quality' : int(jpeg_quality) }
        config = client.update_configuration(params)

if __name__ == '__main__':
    rospy.init_node('nordic_send', anonymous=True)

    set_compressedimage_quality(camera_topic)
    set_compressedimage_quality(hector_topic)

    node = Node()
    node.run()

    

