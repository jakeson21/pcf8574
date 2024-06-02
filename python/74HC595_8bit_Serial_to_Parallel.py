#!/usr/bin/env python3

import time
import smbus2 as smbus
# pip install timeloop
from timeloop import Timeloop
from datetime import timedelta, datetime
# imports random module
import random

tl = Timeloop()

# MAN6980 7-Segment Display with DP
# p0 : SCK
# p1 : SER
# p2 : ~G (output enable)
# p3 : RCK
# p4 : NC
# p5 : NC
# p6 : NC
# p7 : NC

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  PCF8574 defaults to address 0x20
address = 0x20

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

# Shift everything left by 4 bits and separate bytes
rw = 0; # 0=Write, 1=Read
add = (address << 1) + rw

clk = 0
rck = 0
data = 0
G_en_L = 0
count = 0

# Write out I2C command: address, reg_write_dac, msg[0], msg[1]
# bus.write_i2c_block_data(address, add, )
@tl.job(interval=timedelta(seconds=.01))
def counter():
    global clk, rck, data, G_en_L, count
    myobj = datetime.now()
    # s = myobj.second % 10
    print("Current time {}.{:06}".format(myobj.second, myobj.microsecond))

    val = (data << 1) | (G_en_L << 2)
    data = random.randint(0, 1)
    # Set serial data state
    bus.write_byte(address, clk | val)
    # Transfer next into shift registers
    clk = 1
    bus.write_byte(address, clk | val)
    clk = 0
    bus.write_byte(address, clk | val)
    # Contents of shift register transferred to output latches
    if (count % 8 == 0):
        bus.write_byte(address, clk | val | (1 << 3))
        bus.write_byte(address, clk | val)
        count = 0

    count += 1
    
    

if __name__ == "__main__":
    tl.start(block=True)
    bus.close()
