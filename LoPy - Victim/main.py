# Slowly recieves data via I2C, and broadcasts the data via lopy.
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html 
from network import LoRa
from machine import I2C
import socket
import time

lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923) # Operation of unlicensed Part 15 devices are permitted between 902 and 928 MHz
# TODO: After confirming if the slave works, insert I2C code
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) # set data rate
## Info: Value of 0 - 250 bit/s, spreading factor of 12
# TODO: I2C logic to obtain data, and make sure the data is full
s.setblocking(False)

# Is there anyone out there?
while True:
    s.send("Can you hear me?")
    time.sleep(5)
