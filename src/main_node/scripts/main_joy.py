#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy


def main_handler(Joy):
    rospy.loginfo()


def main_joy():
    rospy.init_node('main_joy', anonymous=True)
    rospy.Subscriber('joy_node', Joy, main_handler)
    
    rospy.spin()

if __name__ == '__main__':
    main_joy()