#!/usr/bin/env python
from queue import Empty
import queue
import sys
import struct
from numpy import dtype
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from std_msgs.msg import Empty
from sensor_msgs.msg import Joy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header
from serial import Serial, serialutil
from io import BytesIO
import numpy as np
from ctypes import *
import binascii
import direct_server as direct_server_

import dynamic_reconfigure.client

class Node:
    def __init__(self):
        self.direct_server = rospy.get_param("~direct_server")
        self.enable = rospy.get_param("~enable")
        if self.direct_server:
            self.enable = False
            self.direct_server = direct_server_.Connection(6000)

        camera_topic = rospy.get_param("~camera_topic")
        tilemap_topic = rospy.get_param("~tilemap_topic")
        fullmap_topic = rospy.get_param("~fullmap_topic")
        map_pose_topic = rospy.get_param("~map_pose_topic")
        reply_topic = rospy.get_param("~reply_topic")
        jpeg_quality = rospy.get_param("~jpeg_quality_level")
        render_map_topic = rospy.get_param("~render_map_topic")
        
        self.image_map_ratio = int(rospy.get_param("~image_map_ratio"))

        self.images_sent = 0
        self.camera_image = None
        self.tilemap_image = None
        self.fullmap_image = None
        self.pose_array = 0

        self.set_compressedimage_quality(camera_topic, jpeg_quality)
        self.set_compressedimage_quality(tilemap_topic, jpeg_quality)
        self.set_compressedimage_quality(fullmap_topic, jpeg_quality)

        self.dev = rospy.get_param("~dev", "/dev/ttyACM0")
        self.baud = int(rospy.get_param("~baud", "115200"))

        self.sent_messages = 0

        if self.enable:
            rospy.loginfo("Nordic_send - opening serial " + self.dev)
            self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)

        self.sub_camera = rospy.Subscriber(camera_topic, CompressedImage, self.callback_camera)
        rospy.loginfo("Nordic_send - subscribed to topic " + camera_topic)
        
        self.sub_tile = rospy.Subscriber(tilemap_topic, CompressedImage, self.callback_tilemap)
        rospy.loginfo("Nordic_send - subscribed to topic " + tilemap_topic)
        
        self.send_reply = rospy.Subscriber(reply_topic, Bool, self.callback_reply)
        rospy.loginfo("Nordic_send - subscribed to topic " + reply_topic)
        
        self.pub_render = rospy.Publisher(render_map_topic, Bool, queue_size = 1)
        rospy.loginfo("Nordic_send - published topic " + render_map_topic)
        
        self.sub_pose = rospy.Subscriber(map_pose_topic, PoseStamped, self.callback_pose)
        rospy.loginfo("Nordic_send - subscribed to topic " + map_pose_topic)

        self.sub_fullmap = rospy.Subscriber(fullmap_topic, CompressedImage, self.callback_fullmap)
        rospy.loginfo("Nordic_send - subscribed to topic " + fullmap_topic)

    def run(self):
        rospy.spin()

    # pickup from callback_reply
    def callback_fullmap(self, fullmap_image):
        rospy.loginfo("Nordic_send - sending fullmap image")

        fullmap_image.header.frame_id = "full"

        # fill header data with adjusted pose data. don't holla at me, I know its janky
        # seq is uint32, so max map coords can be 65535, 65535 but by god I hope the image isn't that large
        fullmap_image.header.seq = self.pose_array

        self.send_compressed_image(fullmap_image)

    def callback_reply(self, boolean):
        # deploy node
        if boolean.data:
            # initialize node deployment
            self.send_node_init()
            self.pub_render.publish(boolean)
            # this will pick up on callback

        else:
            if self.images_sent < self.image_map_ratio:
                rospy.loginfo("Nordic_send - sending camera image")
                if not self.camera_image:
                    return
                self.send_compressed_image(self.camera_image)
                self.images_sent += 1
                if self.images_sent == self.image_map_ratio:
                    # render the tilemap for the next time around
                    self.pub_render.publish(boolean)
            else:
                rospy.loginfo("Nordic_send - sending tilemap image")
                self.images_sent = 0
                if not self.tilemap_image:
                    return
                self.tilemap_image.header.seq = self.pose_array
                self.send_compressed_image(self.tilemap_image)

    def callback_pose(self,poseStamped):
        self.pose_array = self.two_uint16_to_uint32(poseStamped.pose.position.x, poseStamped.pose.position.y)

    def callback_camera(self, compressedImage):
        compressedImage.header.frame_id = "cam"
        compressedImage.header.seq = 0
        self.camera_image = compressedImage

    def callback_tilemap(self, compressedImage):
        compressedImage.header.frame_id = "tile"
        self.tilemap_image = compressedImage

    def send_compressed_image(self, compressedImage):
        if self.sent_messages == 1:
           return

        self.sent_messages += 1
        self.write_buffer(compressedImage)

    def write_buffer(self, compressedImage):
        buffer = BytesIO()
        compressedImage.serialize(buffer)

        if self.enable:
            self.send_as_chunks(buffer.getvalue())
        if self.direct_server:
            print(str(len(buffer.getvalue())))
            print(binascii.hexlify(buffer.getvalue()))
            self.direct_server.send_data(buffer.getvalue())

    def set_compressedimage_quality(self, topic, quality):
        client = dynamic_reconfigure.client.Client(topic, timeout = 3)
        client.update_configuration({ 'format' : 'jpeg', 'jpeg_quality' : int(quality)})
        return

    def send_as_chunks(self, data):
        size = len(data)
        rospy.loginfo("Message length: " + str(size))
        n = 64

        #rospy.loginfo(binascii.hexlify(data))

        rospy.loginfo("Nordic_send - starting send")
        
        chunks = [data[i:i+n] for i in range(0, size, n)]

        last_packet = len(chunks[-1])
        last_packet_byte = bytes(struct.pack("B", last_packet))

        #print("last_packet: " + str(last_packet))
        #print("last_packet_bytes: " + binascii.hexlify(last_packet_byte))

        chunks.insert(0,b'start'+last_packet_byte)
        chunks.append(b'end')

        print("Num packets: " + str(len(chunks)))

        for chunk in chunks:
            #self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)
            self.serial.write(chunk)
            #print(str(len(chunk)))
            print(binascii.hexlify(chunk))

        rospy.loginfo("Nordic_send - finish send")

    def two_uint16_to_uint32(self, firstval, secondval):
        return c_uint32(c_uint32(int(firstval) << 16).value | int(secondval)).value

if __name__ == '__main__':
    rospy.init_node('nordic_send', anonymous=True)
    node = Node()
    node.run()

    

