#!/usr/bin/env python
import struct
import numpy as np


val = np.int8(-1 * 127)

print (val.tobytes())


print(np.float64((np.int8(-1 * 127)/127)))

def int8_to_float64(uint8val):
    val = np.float64(uint8val/127)
    return (np.float64())


    