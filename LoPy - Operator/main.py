# Recieves data from the LoRa network, and publishes data via POST to the dashboard
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html, https://docs.pycom.io/tutorials/all/wlan.html, and https://tools.ietf.org/html/rfc2616#section-4
# Comment style: # for normal comments, ## for theory / personal comments
## Yes, I linked RFC2616, the document for HTTP/1.1. There's no native HTTP implementation.


from network import LoRa, WLAN
import machine
import socket

# Constants
WIFI_SSID = "<WiFi SSID Here>"
WIFI_PASSWORD = "<WiFi password here>"
POST_IP = "<server ip here>"
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

# Do work with data
if __name__ == "__main__":
    buf = b''
    while True:
        buf.join(s.recv(64))

        # Verify the buffer
        if buf.count(",") != 4:
            continue # we haven't recieved the full buffer

        # Send the buffer
        http_post(POST_IP, POST_PORT, buf)
