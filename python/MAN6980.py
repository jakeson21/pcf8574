#!/usr/bin/env python3

import time
import smbus2 as smbus
# pip install timeloop
from timeloop import Timeloop
from datetime import timedelta, datetime


tl = Timeloop()

# MAN6980 7-Segment Display with DP
# p0 : A
# p2 : B
# p2 : C
# p3 : D
# p4 : E
# p5 : F
# p6 : G
# p7 : DP
# All LEDs are driven from 5V through 150 ohm into package pins.
# PCF8574 connected to package pins as pull-downs to turn off LEDs. 

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  PCF8574 defaults to address 0x20
address = 0x20

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

# Shift everything left by 4 bits and separate bytes
rw = 0; # 0=Write, 1=Read
add = (address << 1) + rw

# 7-Segment decoder map
decode = {0: 0b00111111,
        1:   0b00000110,
        2:   0b01011011,
        3:   0b01001111,
        4:   0b01100110,
        5:   0b01101101,
        6:   0b01111101,
        7:   0b00000111,
        8:   0b01111111,
        9:   0b01100111}

dp = 0b10000000
with_dp = 0xFF

# Write out I2C command: address, reg_write_dac, msg[0], msg[1]
# bus.write_i2c_block_data(address, add, )
@tl.job(interval=timedelta(seconds=.1))
def counter():
    global with_dp
    myobj = datetime.now()
    s = myobj.second % 10
    print("Current microsecond ", myobj.microsecond)
    bus.write_byte(address, decode[s] | dp*with_dp)
    with_dp ^= 0xFF

if __name__ == "__main__":
    tl.start(block=True)
    bus.close()
