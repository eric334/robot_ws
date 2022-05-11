#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy
from serial import Serial, serialutil
import StringIO
import sys

# recieve data messages from nordic, get message type and publish
class Node:
    def __init__(self):
        self.enable = rospy.get_param("~enable")

        maestro_topic = rospy.get_param("~maestro_topic")
        roboclaw_topic = rospy.get_param("~roboclaw_topic")
        reply_topic = rospy.get_param("~reply_topic")

        self.dev = rospy.get_param("~dev", "/dev/ttyACM0")
        self.baud = int(rospy.get_param("~baud", "115200"))
        
        if self.enable:
            rospy.loginfo("Nordic_recv - opening serial : " + self.dev)
            self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)

        self.pub_maestro = rospy.Publisher(maestro_topic, Empty, queue_size =1)
        rospy.loginfo("Nordic_recv - published topic : " + maestro_topic)
        
        self.pub_roboclaw = rospy.Publisher(roboclaw_topic, Twist, queue_size=1)
        rospy.loginfo("Nordic_recv - published topic : " + roboclaw_topic)
        
        self.pub_reply = rospy.Publisher(reply_topic, Bool, queue_size=1)
        rospy.loginfo("Nordic_recv - published topic : " + reply_topic)


    def run(self):
        if not self.enable:
            rospy.spin()

        #rate = rospy.Rate(100)

        message = b''
        last_packet = 0

        while not rospy.is_shutdown():
            bytesToRead = self.serial.inWaiting()
            data = self.serial.read(bytesToRead)

            data = data[:64]
            
            if data[0:5] == b'start':
                print(binascii.hexlify(data))
                print(type(data))
                print("last_packet bytes: " + str(binascii.hexlify(data[5:6])))
                last_packet = int.from_bytes(data[5:6], 'big')
                print ("last_packet: " + str(last_packet))
                message = b''
            elif data[0:3] == b'end':
                twistStamped = TwistStamped()

                message = message[:len(message) - 64 + last_packet]
                #print("Entire message: \n " + str(binascii.hexlify(message)))

                try:
                    buffer = BytesIO(message)
                    twistStamped.deserialize(buffer.getvalue())
                except:
                    rospy.logerr("Deserialization of message failed, traceback: \n" + traceback.format_exc())

                #print(compressedImage)

                boolean = Bool()
                boolean.data = False
                if twistStamped.header.frame_id == "con":
                    self.pub_roboclaw.publish(twistStamped.twist)
                elif twistStamped.header.frame_id == "condep":
                    # deploy node
                    boolean.data = True
                    self.pub_roboclaw.publish(Twist())
                    self.pub_maestro.publish(Empty())
                else:
                    rospy.logerr("Unrecognized frame id found: "+ twistStamped.header.frame_id)

                # initiate send back message
                self.pub_reply.publish(boolean)

            elif data != b'':
                #print(len(data))
                #print(binascii.hexlify(data))
                message += data
            
            # rate.sleep()


if __name__ == '__main__':
    rospy.init_node('nordic_recv', anonymous=True)
    node = Node()
    node.run()
