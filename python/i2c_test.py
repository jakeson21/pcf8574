#!/usr/bin/env python3

import time
import smbus2 as smbus


# I2C channel 1 is connected to the GPIO pins
channel = 1

#  PCF8574 defaults to address 0x20
address = 0x20

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

# Shift everything left by 4 bits and separate bytes
rw = 0; # 0=Write, 1=Read
add = (address << 1) + rw
msg_on = 0xFF
msg_off = 0x00
msg_on_off = [msg_on, msg_off]*16

# Write out I2C command: address, reg_write_dac, msg[0], msg[1]
# bus.write_i2c_block_data(address, add, )
while True:
    # bus.write_i2c_block_data(address, add, msg_on)
    # time.sleep(0.000)
    # bus.write_i2c_block_data(address, add, msg_off)
    # time.sleep(0.000)

    # bus.write_i2c_block_data(address, msg_off, msg_on_off) # Achieves ~3kHz

    # bus.write_byte_data(address, msg_on, msg_off) # Achieves ~2kHz

    msg_off += 1
    time.sleep(0.050)
    bus.write_byte(address, 0xFF ^ 0b10101010)
