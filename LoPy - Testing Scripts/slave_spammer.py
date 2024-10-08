# Slowly recieves data via I2C, and broadcasts the data via lopy.
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html 
from network import LoRa
from machine import UART
import socket
import time

TX_PIN = "G17"
RX_PIN = "G22"

lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923) # Operation of unlicensed Part 15 devices are permitted between 902 and 928 MHz
uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, pins=(TX_PIN, RX_PIN))
# TODO: After confirming if the slave works, insert I2C code
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) # set data rate
## Info: Value of 0 - 250 bit/s, spreading factor of 12
# TODO: I2C logic to obtain data, and make sure the data is full

while True:
    s.setblocking(False)
    s.send(b'0,16/12/18 11:08,51.174693,-3.061574,0')
    s.settimeout(5)
    try:
        ok_message = s.recv(64)
    except TimeoutError:
        continue

    if ok_message[0] != 35 or ok_message[-1] != 35:
        continue
    print(ok_message[1:-1])
    time.sleep(5)
