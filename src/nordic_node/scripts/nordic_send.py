#!/usr/bin/env python
from queue import Empty
import queue
import sys

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

import dynamic_reconfigure.client

class Node:
    def __init__(self):
        self.enable = rospy.get_param("~enable")

        camera_topic = rospy.get_param("~camera_topic")
        tilemap_topic = rospy.get_param("~tilemap_topic")
        self.fullmap_topic = rospy.get_param("~fullmap_topic")
        self.map_pose_topic = rospy.get_param("~map_pose_topic")
        reply_topic = rospy.get_param("~reply_topic")
        jpeg_quality = rospy.get_param("~jpeg_quality_level")
        render_map_topic = rospy.get_param("~render_map_topic")
        
        self.image_map_ratio = int(rospy.get_param("~image_map_ratio"))

        self.images_sent = 0
        self.camera_image = None
        self.tilemap_image = None
        self.fullmap_image = None
        self.pose_array = None

        self.set_compressedimage_quality(camera_topic, jpeg_quality)
        self.set_compressedimage_quality(tilemap_topic, jpeg_quality)
        self.set_compressedimage_quality(self.fullmap_topic, jpeg_quality)

        self.dev = rospy.get_param("~dev", "/dev/ttyACM0")
        self.baud = int(rospy.get_param("~baud", "115200"))

        if self.enable:
            rospy.loginfo("Nordic_send - opening serial " + self.dev)
            self.serial = Serial(self.dev, timeout=1, baudrate=self.baud)

        self.sub_camera = rospy.Subscriber(camera_topic, CompressedImage, self.callback_camera)
        rospy.loginfo("Nordic_send - subscribed to topic " + camera_topic)
        self.sub_tile = rospy.Subscriber(tilemap_topic, CompressedImage, self.callback_tilemap)
        rospy.loginfo("Nordic_send - subscribed to topic " + tilemap_topic)
        self.send_reply = rospy.Subscriber(reply_topic, Bool, self.callback_reply)
        rospy.loginfo("Nordic_send - subscribed to topic " + reply_topic)
        self.render_map = rospy.Publisher(render_map_topic, Bool, queue_size = 1)
        rospy.loginfo("Nordic_send - published topic " + render_map_topic)
        self.pose_topic = rospy.Subscriber(self.map_pose_topic, PoseStamped, self.callback_pose)
        rospy.loginfo("Nordic_send - published topic " + self.map_pose_topic)

        # USE ONLY FOR RQT_GRAPH VISUALIZATION, WILL CAUSE FULL RENDERS ALL THE TIME
        self.pose_topic = rospy.Subscriber(self.fullmap_topic, CompressedImage, None)

        # initialize loop with remote station
        self.init_connection = True    

    def run(self):
        rospy.spin()

    def callback_reply(self, boolean):
        # deploy node
        if boolean.data:
            # initialize node deployment
            self.send_node_init()
            # render full map starting now
            # subscribed and unsubscribe so that the full map is not always rendered
            sub_fullmap = rospy.Subscriber(self.fullmap_topic, CompressedImage, self.callback_fullmap)
            rospy.loginfo("Nordic_send - subscribed to topic " + self.fullmap_topic)

            self.render_map.publish(boolean)

            self.fullmap_image = rospy.wait_for_message(self.fullmap_topic, CompressedImage)
            self.fullmap_image.header.frame_id = "full"

            # fill header data with adjusted pose data. don't holla at me, I know its janky
            # pid is uint32, so max map coords can be 65535, 65535 but by god I hope the image isn't that large
            self.fullmap_image.header.pid = self.pose_array

            self.send_compressed_image(self.fullmap_image)

            rospy.loginfo("Nordic_send - unsubscribed from topic " + self.tilemap_topic)
            sub_fullmap.shutdown()
        else:
            if self.images_sent < self.image_map_ratio:
                self.send_compressed_image(self.camera_image)
                self.images_sent += 1
                if self.images_sent == self.image_map_ratio:
                    # render the tilemap for the next time around
                    self.render_map.publish(boolean)
            else:
                self.images_sent = 0
                self.tilemap_image.pid = self.pose_array
                self.send_compressed_image(self.tilemap_image)

    def callback_pose(self,poseStamped):
        self.pose_array = np.array([poseStamped.pose.position.x, poseStamped.pose.position.y], dtype = np.uint16)

    def callback_camera(self, compressedImage):
        compressedImage.header.frame_id = "cam"
        self.camera_image = compressedImage

        if self.init_connection:
            self.init_connection = False
            boolean = Bool()
            boolean.data = False
            self.callback_reply(boolean)

    def callback_tilemap(self, compressedImage):
        compressedImage.header.seq = self.pose_array
        compressedImage.header.frame_id = "tile"
        self.tilemap_image = compressedImage

    def send_compressed_image(self, compressedImage):
        if self.enable:
            self.write_serial(compressedImage)

    def write_serial(self, compressedImage):
        buffer = BytesIO()
        compressedImage.serialize(buffer)
        self.send_as_chunks(buffer.getvalue())

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

    

