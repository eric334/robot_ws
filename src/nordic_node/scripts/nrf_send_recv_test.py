# https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py

#!/usr/bin/env python
import sys
import os
import time
from pympler.asizeof import asizeof
from serial import Serial, serialutil

dev = '/dev/ttyACM0'
baud = 115200

serial = Serial(dev, timeout=1, baudrate=baud)
serial.close()
serial.open()


# for i in range(10):
#     # string = "test" + str(i)
#     # print("send: " + string)
#     # serial.write("0010".encode())
#     # bytesToRead = 0
#     # while bytesToRead == 0:
#     #     bytesToRead = serial.inWaiting()
#     # data = serial.read(bytesToRead)
#     # print(data)

def send_size_then_data(data):
    data = b''.join([b'0000', bytes(data)])
    size = asizeof(data)

    print ("actual size " + str(size))
    print ("system size " + str(sys.getsizeof(data)))

    if (size > 9999):
        rospy.logerror("fatal error size larger than 9999 bytes")
        return

    size = str(size).zfill(4)

    print("sending " + size)

    serial.write(size.encode())

    bytesToRead = 0
    while bytesToRead == 0:
        bytesToRead = serial.inWaiting()
    echo = serial.read(bytesToRead)
    print("echo " + echo)

    serial.write(data)


send_size_then_data("ut I must explain to you how all this\n mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete \naccount of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?ut I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?ut I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?ut I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
bytesToRead = 0
while bytesToRead == 0:
    bytesToRead = serial.inWaiting()
echo = serial.read(bytesToRead)
print("echo: " + echo)

    