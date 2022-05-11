#!/usr/bin/env python
import queue
import rospy
from std_msgs.msg import Empty
from nav_msgs.msg import OccupancyGrid
import os
import time

# this node controls the map such that the image map renderer is not rendering on each update
class Node:
    def __init__(self):
        map_sub_topic = rospy.get_param("~map_sub_topic")
        map_pub_topic = rospy.get_param("~map_pub_topic")
        map_output_topic = rospy.get_param("~map_output_topic")

        self.map = None

        self.map_sub = rospy.Subscriber(map_sub_topic, OccupancyGrid, self.callback_map)
        rospy.loginfo("Map_control - subscribed topic : " + map_sub_topic)
        self.map_pub = rospy.Publisher(map_pub_topic, OccupancyGrid, queue_size=1)
        rospy.loginfo("Map_control - published topic : " + map_pub_topic)
        self.map_output = rospy.Subscriber(map_sub_topic, OccupancyGrid, self.callback_map_output)
        rospy.loginfo("Map_control - published topic : " + map_output_topic)

    def run(self):
        rospy.spin()

    def callback_map(self, occupancyGrid):
        self.map = occupancyGrid

    def callback_map_output(self, empty):
        self.map_pub.publish(self.map)
        

if __name__ == '__main__':
    rospy.init_node('map_control_node', anonymous=True)
    node = Node()
    node.run()
