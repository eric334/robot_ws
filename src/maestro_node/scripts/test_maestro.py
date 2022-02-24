import os
import time

os.system('mono ./UscCmd --servo 0,9984')
time.sleep(3)
os.system('mono ./UscCmd --servo 0,1984')
