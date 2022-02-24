#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
import os
import time

class maestroClass:

    def __init__(self):
        self._sub = rospy.Subscriber('main_maestro_activate', Bool, self._callback)

        rospy.spin()

    def _callback(self, data):
        if (data):
            os.system('mono ./UscCmd --servo 0,9984')
            time.sleep(3)
            os.system('mono ./UscCmd --servo 0,1984')
        

if __name__ == '__main__':
    rospy.init_node('maestro_controller', anonymous=True)
    maestroClass = maestroClass()