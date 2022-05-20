#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
import os
import time
import rospkg

class Node:

    def __init__(self):
        rospack = rospkg.RosPack()
        self.cwd = rospack.get_path('maestro_node')
        rospy.loginfo("Maestro node cwd: " +  str(self.cwd))

        subscribed_topic = rospy.get_param("~subscribed_topic", "")

        self._sub = rospy.Subscriber(subscribed_topic, Empty, self.callback)
        rospy.loginfo("Maestro - subscribed topic : " + subscribed_topic)

    def run(self):
        rospy.spin()

    def callback(self, data):
        os.system('mono '+str(self.cwd)+'/scripts/UscCmd --servo 0,1000')
        time.sleep(4.065)
        os.system('mono '+str(self.cwd)+'/scripts/UscCmd --servo 0,0')
        time.sleep(1)
        os.system('mono '+str(self.cwd)+'/scripts/UscCmd --servo 0,50000')
        time.sleep(4.065)
        os.system('mono '+str(self.cwd)+'/scripts/UscCmd --servo 0,0')

if __name__ == '__main__':
    rospy.init_node('maestro_node', anonymous=True)
    node = Node()
    node.run()
