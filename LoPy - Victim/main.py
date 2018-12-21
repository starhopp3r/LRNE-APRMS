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
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) # set data rate
## Info: Value of 0 - 250 bit/s, spreading factor of 12

# Every 30 seconds, attempts to obtain data from the UART
while True:
    if uart.any():
        data = uart.readline()
        uart.readall() # purge remaining data
        print(data)
        if data.count(b',') != 4: # check to ensure that we have 4 parameters
            continue
       
        s.setblocking(False)
        s.send(data[:-1]) # otherwise, sends the data, omitting the \n character

        s.settimeout(5)
        try:
            broadcast = s.recv(256) # recieves the broadcast message back
        except TimeoutError:
            continue

        if broadcast[1] != b'#' or broadcast[-1] != b'#': # ensures that the message is ours
            continue

        print(broadcast)
