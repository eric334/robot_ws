#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header
from serial import Serial, serialutil

import dynamic_reconfigure.client

class Node:
    def __init__(self):
        self.enable = rospy.get_param("~enable")

        camera_topic = rospy.get_param("~camera_topic")
        hector_topic = rospy.get_param("~hector_topic")
        jpeg_quality = rospy.get_param("~jpeg_quality_level")

        self.set_compressedimage_quality(camera_topic, jpeg_quality)
        self.set_compressedimage_quality(hector_topic, jpeg_quality)

        self.dev = rospy.get_param("~dev", "/dev/ttyACM0")
        self.baud = int(rospy.get_param("~baud", "115200"))

        if self.enable:
            rospy.loginfo("Nordic_send - opening serial : " + self.dev)
            self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)

        self.sub_camera = rospy.Subscriber(camera_topic, CompressedImage, self.callback_camera)
        rospy.loginfo("Nordic_send subscribed to topic : " + camera_topic)
        self.sub_hector = rospy.Subscriber(hector_topic, CompressedImage, self.callback_hector)
        rospy.loginfo("Nordic_send subscribed to topic : " + hector_topic)

    def run(self):
        rospy.spin()

    def callback_hector(self, compressedImage):
        if self.enable:
            compressedImage.header.frame_id = "hec"
            self.write_serial(compressedImage)

    def callback_camera(self, compressedImage):
        if self.enable:
            compressedImage.header.frame_id = "cam"
            self.write_serial(compressedImage)

    def write_serial(self, compressedImage):
        buffer = BytesIO()
        compressedImage.serialize(buffer)

        self.send_as_chunks(buffer.getvalue())
        return

    def set_compressedimage_quality(self, topic, quality):
        client = dynamic_reconfigure.client.Client(topic, timeout = 3)
        client.update_configuration({ 'format' : 'jpeg', 'jpeg_quality' : int(quality)})
        return

    def send_as_chunks(self, data):
        size = len(data)
        #print("Size: " + str(size))
        n = 64

        #print("Entire message: \n" + binascii.hexlify(data))
        
        chunks = [data[i:i+n] for i in range(0, size, n)]

        last_packet = len(chunks[-1])
        last_packet_byte = bytes(struct.pack("B", last_packet))

        #print("last_packet: " + str(last_packet))
        #print("last_packet_bytes: " + binascii.hexlify(last_packet_byte))

        chunks.insert(0,b'start'+last_packet_byte)
        chunks.append(b'end')

        #print("Num packets: " + str(len(chunks)))

        for chunk in chunks:
            self.serial.write(chunk)
            self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)
            #print(str(len(chunk)))
            #print (binascii.hexlify(chunk)

if __name__ == '__main__':
    rospy.init_node('nordic_send', anonymous=True)
    node = Node()
    node.run()

    

