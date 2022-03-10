#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
import os
import time

subscribed_topic = rospy.get_param("~subscribed_topic", "")

class Node:
    global subscribed_topic

    def __init__(self):
        self._sub = rospy.Subscriber(subscribed_topic, Empty, self.callback)

    def run(self):
        rospy.spin()

    def callback(self, data):
        os.system('mono ./UscCmd --servo 0,9984')
        time.sleep(3)
        os.system('mono ./UscCmd --servo 0,1984')
        

if __name__ == '__main__':
    rospy.init_node('maestro_node', anonymous=True)
    node = Node()
    node.run()