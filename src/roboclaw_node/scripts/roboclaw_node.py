#!/usr/bin/env python

from roboclaw import Roboclaw
import rospy
from geometry_msgs.msg import Quaternion, Twist


max_speed = 127

class Node:
    def __init__(self):
        rospy.on_shutdown(self.stop)

        self.reset_time = 2

        self.enable = rospy.get_param("~enable")

        twist_topic = rospy.get_param("~twist_topic")

        rospy.Subscriber(twist_topic, Twist, self.callback_twist) 

        if not self.enable:
            return

        dev = rospy.get_param("~dev", "/dev/ttyACM0")
        baud = int(rospy.get_param("~baud", "115200"))
        self.address = int(rospy.get_param("~address", "128"))
	
	rospy.loginfo("Roboclaw_node - dev : " + dev)

        self.roboclaw = Roboclaw(dev, baud)

        self.roboclaw.Open()

        # just in case the bootdown was not so good
        self.stop()

        self.speed_multiplier = min(float(rospy.get_param("~speed_multiplier", "1.0")), 127)

        self.latest_set = rospy.get_rostime()


    def run(self):
        if not self.enable:
            rospy.spin()
            return

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            current_time = rospy.get_rostime()
            if (current_time - self.latest_set).to_sec() > self.reset_time:
                self.latest_set = current_time
                rospy.loginfo("Roboclaw_node - no command, stopping motors")
                self.stop()

            rate.sleep()

    def callback_twist(self, twist):
        if not self.enable:
            return

        self.latest_set = rospy.get_rostime()

        right_speed = -1 * int(max(min(twist.linear.x + (-1* twist.angular.z), 1.3), -1.3)  * self.speed_multiplier)
        left_speed = -1 * int(max(min(twist.linear.x - (-1* twist.angular.z), 1.3), -1.3) * self.speed_multiplier)

        print(right_speed)
        print(left_speed)

        if right_speed > 0:
            self.roboclaw.ForwardM1(self.address, right_speed)
        else:
            self.roboclaw.BackwardM1(self.address, right_speed * -1)
        if left_speed > 0:
            self.roboclaw.ForwardM2(self.address, left_speed)
        else:
            self.roboclaw.BackwardM2(self.address, left_speed * -1)

    def stop(self):
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0)

if __name__ == "__main__":
    rospy.init_node("roboclaw_node", anonymous=True)
    node = Node()
    node.run()
