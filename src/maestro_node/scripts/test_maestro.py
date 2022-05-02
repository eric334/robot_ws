import os
import time


os.system('mono ./UscCmd --servo 0,1000')
time.sleep(2.335)
os.system('mono ./UscCmd --servo 0,0')
time.sleep(1)
os.system('mono ./UscCmd --servo 0,50000')
time.sleep(2.35)
os.system('mono ./UscCmd --servo 0,0')

