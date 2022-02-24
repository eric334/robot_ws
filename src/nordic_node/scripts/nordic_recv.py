#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from serial import Serial, serialutil
import StringIO


# message types :
# 00 - Empty type for maestro_node node drop - maestro_recv
# 01 - Twist for roboclaw_node roboclaw motors - roboclaw_recv
# 10 - CompressedImage from camera_node compressed image - compressed_send
# 11 - Data from hector_slam updated slam data - hector_send

# recieve data messages from nordic, get message type and publish
class node:

    def __init__(self):
        dev = rospy.get_param("~dev", "/dev/ttyACM0")
        baud = int(rospy.get_param("~baud", "115200"))
        
        self._ser = Serial(dev, timeout=1, baudrate=baud)

        self._pub = rospy.Publisher('recv_data', Twist)
        self.


    def run(self):
        rate = rospy.Rate(100)

        while not rospy.is_shutdown():
            bytesToRead = _ser.inWaiting()
            data = _ser.read(bytesToRead)
            _pub.publish(hello_str)
            
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node('nordic_recv', anonymous=True)
    node = Node()
    node.run()
