#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from sensor_msgs.msg import Joy
from serial import Serial, serialutil
import StringIO
import sys
import numpy as np

# recieve data messages from nordic, get message type and publish
class Node:
    def __init__(self):
        maestro_topic = rospy.get_param("~maestro_topic")
        roboclaw_topic = rospy.get_param("~roboclaw_topic")

        dev = rospy.get_param("~dev", "/dev/ttyACM0")
        baud = int(rospy.get_param("~baud", "115200"))
        
        rospy.loginfo("Nordic_recv - opening serial : " + dev)
        # TODO COPY SPECIFICS ?
        self.serial = Serial(dev, timeout=1, baudrate=baud)

        self.pub_maestro = rospy.Publisher(maestro_topic, Empty)
        rospy.loginfo("Nordic_recv - published topic : " + maestro_topic)
        self.pub_roboclaw = rospy.Publisher(roboclaw_topic, Twist)
        rospy.loginfo("Nordic_recv - published topic : " + roboclaw_topic)

    def run(self):
        rate = rospy.Rate(100)

        while not rospy.is_shutdown():
            bytesToRead = self.serial.inWaiting()
            data = self.serial.read(bytesToRead)

            array = data.astype(np.unint8)

            # if 0, message is empty message
            if array[0] == 0:
                self.pub_maestro.publish(Empty())

            # if 1, message is 
            elif array[0] == 1:
                self.pub_roboclaw.publish(data)
            else:
                rospy.logdebug("Error: unrecognized message type found: "+message_type)
            
            rate.sleep()

    def float64_to_int8(floatval):
        return (np.int8(floatval * 127))

    def int8_to_float64(int8val):
        return (np.float64(int8val/127))



if __name__ == '__main__':
    rospy.init_node('nordic_recv', anonymous=True)
    node = Node()
    node.run()
