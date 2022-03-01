#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import CompressedImage
from serial import Serial, serialutil

class Node:

    def __init__(self):
        
        dev = rospy.get_param("~dev", "/dev/ttyACM0")
        baud = int(rospy.get_param("~baud", "115200"))
        
        self.serial = Serial(dev, timeout=1, baudrate=baud)

        self._sub = rospy.Subscriber('usb_cam/compressed', CompressedImage, self.callback)
        self._pub = rospy.Subscriber('send_data_map', CompressedImage, self.callback)

    def run(self):
        rospy.spin()

    def callback(self, data):
        self.serial.write(data)


if __name__ == '__main__':
    rospy.init_node('nordic_send', anonymous=True)
    node = Node()
    node.run()
