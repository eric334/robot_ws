#!/usr/bin/env python

import socket
import subprocess
import traceback
import os
import sys
from threading import Thread
import threading


# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP

##hostname = socket.gethostname()
ip = "10.0.1.128"
port = 6000
buffer_size = 8192

local_socket = None
client_socket = None
remote_address = None

try:
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind((ip, port))
    local_socket.settimeout(None)
    local_socket.listen(5)
except Exception:
    print ("Socket creation failed.")
    print(traceback.format_exc())
    local_socket.close()
    local_socket = None

# its a static mess, I know
class Connection:
    def __init__(self):
        pass
        
    def recv_data(self):
        # this works for singular connection
        try:
            self.aquire_connection()
            return client_socket.recv(buffer_size)
        except Exception:
            print ("Data receive failed.")
            print(traceback.format_exc())

    def send_data(self, data):
        try:
            self.aquire_connection()
            client_socket.send(data)
        except Exception:
            print ("Data send failed.")
            print(traceback.format_exc())

    def aquire_connection(self):
        try:
            if not client_socket and local_socket:
                client_socket, remote_address = local_socket.accept()
                client_socket.settimeout(3)
        except Exception:
            print ("Aquire connection failed.")
            print(traceback.format_exc())

    def close_socket(self):
        if client_socket:
            client_socket.close()
            client_socket = None
        if local_socket:
            local_socket.close()
            local_socket = None