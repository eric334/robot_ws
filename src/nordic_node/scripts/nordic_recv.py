#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import Empty
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

        self.dev = rospy.get_param("~dev", "/dev/ttyACM0")
        self.baud = int(rospy.get_param("~baud", "115200"))
        
        rospy.loginfo("Nordic_recv - opening serial : " + self.dev)
        self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)

        self.pub_maestro = rospy.Publisher(maestro_topic, Empty)
        rospy.loginfo("Nordic_recv - published topic : " + maestro_topic)
        self.pub_roboclaw = rospy.Publisher(roboclaw_topic, Twist)
        rospy.loginfo("Nordic_recv - published topic : " + roboclaw_topic)


    def run(self):
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

                if compressedImage.header.frame_id == "con":
                    self.pub_camera.publish(compressedImage)
                elif compressedImage.header.frame_id == "condep":
                    self.pub_hector.publish(compressedImage)
                else:
                    rospy.logerr("Error: unrecognized frame id found: "+ compressedImage.header.frame_id)

                # get node and pir string from end of end packet
                num_nodes = int.from_bytes(data[3:4], 'big')
                pir_string = String()
                pir_string.data = data[4:4+num_nodes].decode("utf-8")
                pub_pir_string.publish(pir_string)

                # initiate send back message
                self.pub_reply.publish(Empty())

            elif data != b'':
                #print(len(data))
                #print(binascii.hexlify(data))
                message += data
            
            # rate.sleep()


if __name__ == '__main__':
    rospy.init_node('nordic_recv', anonymous=True)
    node = Node()
    node.run()
