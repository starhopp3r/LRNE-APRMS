# Slowly recieves data via I2C, and sends them to the LoRa gateway
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/lorawan-otaa.html
from network import LoRa
from machine import I2C
import socket
import time

# Over-The-Air-Authentication (OTAA) EUI and Key
APP_EUI = "801d139051b39f92"
APP_KEY = "466c3dcbf7bb486fa0de09a0be0b211c"

lora = Lora(mode=LoRa.LORAWAN, region=LoRa.AS923) # Operation of unlicensed Part 15 devices are permitted between 902 and 928 MHz
# TODO: After confirming if the slave works, insert I2C code

# Over-The-Air-Authentication (OTAA) to secure radio network
app_eui = ubinascii.unhexlify(APP_EUI)
app_key = ubinascii.unhexlify(APP_KEY)

# Attempt to join the network via OTAA(timeout: 2.5s)
## Info: This function uses the device's EUI
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=2500)

if !lora.has_joined(): # Have we joined the network?
    print("Node cannot join the network.")
    # TODO: Insert function to tell the device we can't connect
    sys.exit(1)

# Create a LoRa socket if successful
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) # set data rate
## Info: Value of 0 - 250 bit/s, spreading factor of 12
