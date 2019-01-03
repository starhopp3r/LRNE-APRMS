# Slowly recieves data via I2C, and broadcasts the data via lopy.
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html 
from network import LoRa
from machine import UART, Pin
from loramesh import Loramesh
import socket
import time
import machine
import pycom
import gc

#TX_PIN = "G22"
#RX_PIN = "G17"
TX_PIN = "P3"
RX_PIN = "P4"

ARDUINO_POWER = "P8"
BUTTON_OF_POWER = "P9" # 10/10 naming scheme

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

print("[Debug] Initializing pins & interrupts")
arduino_power = Pin(ARDUINO_POWER, mode=Pin.OUT, pull=None)
button = Pin(BUTTON_OF_POWER, mode=Pin.IN, pull=Pin.PULL_UP)
button.callback(Pin.IRQ_FALLING, handler=lambda pin_obj: arduino_power.toggle())
print("[Debug] Pin initialization and interrupts set")

print("[Debug] Initializing LoRa")
machine.disable_irq() # critical section
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923) # Operation of unlicensed Part 15 devices are permitted between 902 and 928 MHz
mesh = Loramesh(lora)
while not mesh.is_connected():
    u_print("[Debug - LoRa mesh connecting] Current state %s, Single: %s" % (mesh.cli('state'), mesh.cli('singleton'))) 
print("[Debug] Initialized & connected to mesh.")

# Create socket
print("[Debug] Initializing socket")
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.bind(PORT)
print("[Debug] Socket initialized")

# Create UART
print("[Debug] Initializing UART")
uart = UART(1, baudrate=9600, bits=8, timeout_chars=255, pins=(TX_PIN, RX_PIN))
previous_data = b"#0,,P#"
compass_data = ""
print("[Debug] UART initialized")
# Turn off heartbeat
pycom.heartbeat(False)

neighbors = mesh.neighbors_ip() # first neighbor already knows the master
ip = mesh.ip()
master_ip = ""
while True:
    buf = ""
    # Mesh Networking
    try:
        # React to any IP change
        if not ip == mesh.ip():
            ip = mesh.ip()

        # Check for any incoming messages: MASTER, MSG and ACK
        machine.disable_irq() # enter networking
        buf, recv_addr = s.recvfrom(64)
        machine.enable_irq()  # exit networking
        if len(buf) > 0 and buf != "":
            print("[Debug] Packet recieved from %s: %s" % (recv_addr[0], buf))

            if buf.startswith("MASTER"):
                blink(0xFF0000)
                buf = buf[6:]
                print("[Debug - Recieved Packet] It was a MASTER IP information packet: %s" % (buf))
                master_ip = buf.decode()
                machine.disable_irq() # enter networking
                s.sendto("ACK" + ip, recv_addr)
                machine.enable_irq() # exit networking
                time.sleep(10)
            elif buf.startswith("MSG"):
                blink(0x00FF00)
                buf = buf[3:]
                print("[Debug - Recieved Packet] It was a message: %s" % (buf))
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
                    machine.disable_irq() # enter networking
                    s.sendto("MASTER%s" % (ip), (neighbor, PORT))
                    machine.enable_irq() # exit networking
                    time.sleep(5)

        # Remove any dropped nodes
        neighbors = list(set(neighbors) - (set(neighbors) - set(new_neighbors)))

        # If master_ip exists, and ping is successful, spam them with information
        if not master_ip == "" and not compass_data == "":
            print("[Debug] Master IP exists. Sending compass data")
            blink(0xFFFFFF)
            machine.disable_irq() # enter networking
            s.sendto("MSG%s" % compass_data, (master_ip, PORT)) # otherwise, sends the data, omitting the \n character
            machine.enable_irq() # exit networking
            time.sleep(10)

    except OSError as e:
        print("[Error] An error ocurred while attempting something. Exact error (no. %d): %s" % (e.errno, e))
        if e.errno == "106":
            print("[Error] The error has been documented in issue #15. Neighbors: %s" % (neighbors))

        if e.errno == 12:
            print("[Error] The error has been documented in issue #15. Triggering garbage collector and sleeping for 6 seconds. Current Mem: %s" % (gc.mem_free()))
            gc.collect()
            time.sleep(6)

    # Serial
    machine.disable_irq() # enter serial read
    data = uart.read()
    machine.enable_irq() # exit serial read

    if data == None:
        continue
    elif data.find(b"OK") >= 0: # ready message, respond with previous data
        print("[Debug] OK Message from Arduino")
        machine.disable_irq() # enter serial write
        uart.write(previous_data)
        machine.enable_irq() # exit serial write
    elif data[0] == 35 and data[-1] == 35 and data.count(b",") == 5: # normal operation
        exploded_data = data[1:-1].decode().split(',')
        if exploded_data[-1] == '1':
            print("[Not implemented] Turn off the screen now") # TODO: Turn off screen

        compass_data = ",".join(exploded_data[:-1])
        print("[Debug] Compass data: %s" % (compass_data)) 

        if not buf == b"": 
            exploded_response = buf[1:-1].decode().split('\n')
            if not compass_data == "":
                try:
                    previous_data = "#%s,%s,%s#" % (compass_data.split(',')[-1], exploded_response[0], exploded_response[1])
                except: pass

        print("[Debug] Sending stored data to Arduino: %s" % previous_data)
        machine.disable_irq() # enter serial write
        uart.write(previous_data)
        machine.enable_irq() # enter serial read

    print("[Debug] Serial message was: %s" % (data))
