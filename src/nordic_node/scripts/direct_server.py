#!/usr/bin/env python

import socket
import subprocess
import traceback
import os
import sys
from threading import Thread
import threading
import rospy
import binascii
import struct

chunk_size = 512

class Connection:
    def __init__(self, port):
        self.client_socket = None
        ip = "10.0.1.128"
        try:
            self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.local_socket.bind((ip, port))
            self.local_socket.settimeout(None)
            self.local_socket.listen(5)
        except Exception:
            print ("Socket creation failed.")
            print(traceback.format_exc())
            self.local_socket.close()
            self.local_socket = None
        
    def recv_data(self):
        # this works for singular connection
        try:
            self.aquire_connection()
            size = struct.unpack(">i",self.client_socket.recv(4))[0]
        
            message = b''
            remaining_size = size
            while len(message) < size:
                recv_size = chunk_size
                if remaining_size < chunk_size:
                    recv_size = remaining_size
                data = self.client_socket.recv(chunk_size)
                print(len(data))
                message += data

            message = message[:size]
            return message

        except Exception:
            print ("Data receive failed.")
            print(traceback.format_exc())

    def send_data(self, data):
        try:
            self.aquire_connection()
            self.client_socket.send(data)
        except Exception:
            print ("Data send failed.")
            print(traceback.format_exc())

    def aquire_connection(self):
        try:
            if not self.client_socket and self.local_socket:
                self.client_socket, self.remote_address = self.local_socket.accept()
                self.client_socket.settimeout(10)
        except Exception:
            print ("Aquire connection failed.")
            print(traceback.format_exc())

    def close_socket(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        if self.local_socket:
            self.local_socket.close()
            self.local_socket = None

if __name__ == '__main__':
    connection = Connection(6000)
    data = connection.recv_data()

    print(str(len(data)))
    print(str(binascii.hexlify(data)))

    connection.close_socket()