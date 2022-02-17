#!/usr/bin/env python
import rospy
from std_msgs.msg import String
# https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py

def main_handler(data):
    rospy.loginfo(data.data)


def main_recv():
    rospy.init_node('main_recv', anonymous=True)
    rospy.Subscriber('main_line', String, main_handler)
    
    rospy.spin()

if __name__ == '__main__':
    main_recv()