# Recieves data from the LoRa network, and publishes data via POST to the dashboard
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html, https://docs.pycom.io/tutorials/all/wlan.html, and https://tools.ietf.org/html/rfc2616#section-4
# Comment style: # for normal comments, ## for theory / personal comments
## Yes, I linked RFC2616, the document for HTTP/1.1. There's no native HTTP implementation.


from network import LoRa, WLAN
from loramesh import Loramesh
import gc
import machine
import socket
import pycom
import utime

# Constants
WIFI_SSID = "<wifi ssid here>"
WIFI_PASSWORD = "<wifi password here>"
POST_IP = "<dashboard ip here>"
POST_PORT = 5000

PORT = 1000

# Function to print changes in strings
old = ""
def u_print(new):
    global old
    if new != old:
        print(new)
        old = new

# TCP Socket init + HTTP post function
def http_post(addr, port, data):
    tcp_s = socket.socket()
    __data = bytes("POST /inlet HTTP/1.1\r\nHost: {:s}:{:d}\r\nContent-Type: text/plain\r\nContent-Length: {:d}\r\n\r\n".format(addr, port, len(data)), "utf8") + data # data is already bytes
    tcp_s.connect(socket.getaddrinfo(addr, port)[0][-1])
    tcp_s.send(__data)
    tcp_s.setblocking(True)
    ok_message = tcp_s.recv(256)
    tcp_s.close()
    return strip_headers(ok_message)

# Discards all the HTTP headers until the body
def strip_headers(data):
    return data.split(b"\r\n")[-1]

# LoRa init
print("[Debug] Initializing LoRa")
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)
mesh = Loramesh(lora)
while not mesh.is_connected():
    u_print("[Debug - LoRa mesh connecting] Current state: %s, Single: %s" % (mesh.cli('state'), mesh.cli('singleton')))
print("[Debug] Initialized & connected to mesh.")

print("[Debug] Connecting to WiFi")
# WLAN init
wlan = WLAN(mode=WLAN.STA)
networks = wlan.scan()
for network in networks:
    if network.ssid == WIFI_SSID:
        wlan.connect(network.ssid, auth=(network.sec, WIFI_PASSWORD), timeout=5000)
        while not wlan.isconnected():
            continue
print("[Debug] Connected to WiFi.")

print("[Debug] Initializing socket")
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.bind(PORT)

# Begin socializing with other neighbors and perform transactions with data
neighbors = []
ip = mesh.ip()
if __name__ == "__main__":
    buf = ""

    while True:
        # Check if this particular node has changed IP addresses
        if not ip == mesh.ip():
            ip = mesh.ip()
            neighbors = [] # if there was an IP change, inform everybody

        # Check the neighbors list, and submit our IP to them.
        new_neighbors = mesh.neighbors_ip()
        diff_neighbors = set(new_neighbors)- set(neighbors)
        u_print("[Debug] Neighbors not acknowledged: %s" % diff_neighbors)
        for neighbor in diff_neighbors:
            if mesh.ping(neighbor) > 0:
                s.sendto("MASTER%s" % (ip), (neighbor, PORT))

        # Remove any dropped nodes
        neighbors = list(set(neighbors) - (set(neighbors) - set(new_neighbors)))
        gc.collect() # run garbage collection

        # There are three possible messages: MASTER, MSG and ACK. Beacuse we are the master, ignore MASTER messages
        buf, recv_addr = s.recvfrom(512)
        if len(buf) > 0 and buf != "":
            print("[Debug] Packet recieved from %s: %s" % (recv_addr[0], buf))

            if buf.startswith("MSG"):
                buf = buf[3:]
                print("[Debug - Recieved Packet] It was a message: %s" % (buf))
                # Verify the buffer
                if buf.count(b",") != 4:
                    continue # we haven't recieved the full buffer

                # Send the buffer to the server
                ok_message = http_post(POST_IP, POST_PORT, buf)

                # Transmit the ok message back to the slave
                if mesh.ping(recv_addr[0]) > 0:
                    s.sendto("MSG" + ok_message.decode(), recv_addr)
            elif buf.startswith("ACK"):
                buf = buf[3:]
                print("[Debug - Recieved Packet] It was an acknowledgement for neighbor discovery, from: %s" % (buf.decode()))
                neighbors.append(buf.decode())
