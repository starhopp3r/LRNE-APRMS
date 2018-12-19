# A complete testing script that occurs entirely between 2 LoPys to test all the intermediaries required
from network import LoRa, WLAN
import machine
import socket

# Constants
WIFI_SSID = "<wifi ssid here>"
WIFI_PASSWORD = "<wifi password here>"
POST_IP = "<dashboard ip here>"
POST_PORT = 5000

# LoRa init
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# WLAN init
wlan = WLAN(mode=WLAN.STA)
networks = wlan.scan()
for network in networks:
    if network.ssid == WIFI_SSID:
        wlan.connect(network.ssid, auth=(network.sec, WIFI_PASSWORD), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # system timer will constantly wake the LoPy

# TCP Socket init + HTTP post function
def http_post(addr, port, data):
    tcp_s = socket.socket()
    __data = bytes("POST /inlet HTTP/1.1\r\nHost: {:s}:{:d}\r\nContent-Type: text/plain\r\nContent-Length: {:d}\r\n\r\n".format(addr, port, len(data)), "utf8") + data # data is already bytes
    tcp_s.connect(socket.getaddrinfo(addr, port)[0][-1])
    tcp_s.send(__data)
    tcp_s.recv(256)
    tcp_s.close()

from machine import UART
uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, pins=("G22", "G17"))
uart.write(b"0,16/12/18 11:08,51.174693,-3.061574,11\n")

# Do work with data
if __name__ == "__main__":
    buf = b''
    while True:
        buf = s.recv(64)

        # Verify the buffer
        if buf.count(b",") != 4:
            continue # wrong data

        # Send the buffer
        http_post(POST_IP, POST_PORT, buf)
