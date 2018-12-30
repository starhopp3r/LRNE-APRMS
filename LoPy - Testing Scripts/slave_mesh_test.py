# Slowly recieves data via I2C, and broadcasts the data via lopy.
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html 
from network import LoRa
from machine import UART
from loramesh import Loramesh
import socket
import time
import machine
import pycom
import gc

TX_PIN = "G17"
RX_PIN = "G22"

PORT = 1000

# Function to print changes in strings
old = ""
def u_print(new):
    global old
    if new != old:
        print(new)
        old = new

# A blink function.
def blink(color):
    pycom.rgbled(color)
    time.sleep_ms(100)
    pycom.rgbled(0x000000)

print("Warning: You are in a testing script. Please use the production version of the script, if available.")
print("[Debug] Initializing LoRa")
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923) # Operation of unlicensed Part 15 devices are permitted between 902 and 928 MHz
mesh = Loramesh(lora)
uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, pins=(TX_PIN, RX_PIN))
while not mesh.is_connected():
    u_print("[Debug - LoRa mesh connecting] Current state %s, Single: %s" % (mesh.cli('state'), mesh.cli('singleton'))) 
print("[Debug] Initialized & connected to mesh.")

# Create socket
print("[Debug] Initializing socket")
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.bind(PORT)
print("[Debug] Socket initialized")

# Turn off heartbeat
pycom.heartbeat(False)

neighbors = mesh.neighbors_ip() # first neighbor already knows the master
ip = mesh.ip()
master_ip = ""
while True:
    buf = ""

    try:
        # React to any IP change
        if not ip == mesh.ip():
            ip = mesh.ip()

        # Check for any incoming messages: MASTER, MSG and ACK
        buf, recv_addr = s.recvfrom(64)
        if len(buf) > 0 and buf != "":
            print("[Debug] Packet recieved from %s: %s" % (recv_addr[0], buf))

            if buf.startswith("MASTER"):
                blink(0xFF0000)
                buf = buf[6:]
                print("[Debug - Recieved Packet] It was a MASTER IP information packet: %s" % (buf))
                master_ip = buf.decode()
                s.sendto("ACK" + ip, recv_addr)
                time.sleep(10)
            elif buf.startswith("MSG"):
                blink(0x00FF00)
                buf = buf[3:]
                print("[Debug - Recieved Packet] It was a message: %s" % (buf))
                # TODO: Serial
            elif buf.startswith("ACK"):
                blink(0x0000FF)
                buf = buf[3:]
                print("[Debug - Recieved Packet] It was an acknowledgement for neighbor discovery, from: %s" % (buf.decode()))
                neighbors.append(buf.decode())

        # Check the neighbors list, and submit the master IP to them, if we have the master IP.
        new_neighbors = mesh.neighbors_ip()
        if not master_ip == "":
            diff_neighbors = set(new_neighbors) - set(neighbors)
            u_print("[Debug] Neighbors not acknowledged: %s" % diff_neighbors)
            for neighbor in diff_neighbors:
                if not neighbor == master_ip:
                    s.sendto("MASTER%s" % (ip), (neighbor, PORT))
                    time.sleep(5)

        # Remove any dropped nodes
        neighbors = list(set(neighbors) - (set(neighbors) - set(new_neighbors)))

        # NOTE: Only in the testing script
        # If master_ip exists, and ping is successful, spam them with information
        if not master_ip == "":
            print("[Debug] Master IP exists. Sending test data")
            blink(0xFFFFFF)
            s.sendto("MSG0,16/12/18 11:08,51.174693,-3.061574,11", (master_ip, PORT)) # otherwise, sends the data, omitting the \n character
            time.sleep(10)

    except OSError as e:
        print("[Error] An error ocurred while attempting something. Exact error (no. %d): %s" % (e.errno, e))
        if e.errno == "106":
            print("[Error] The error has been documented in issue #15. Neighbors: %s" % (neighbors))
            continue

        if e.errno == 12:
            print("[Error] The error has been documented in issue #15. Triggering garbage collector and sleeping for 6 seconds. Current Mem: %s" % (gc.mem_free()))
            gc.collect()
            time.sleep(6)
