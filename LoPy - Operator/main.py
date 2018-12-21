# Recieves data from the LoRa network, and publishes data via POST to the dashboard
# Author: s u d o _
# Reference: https://docs.pycom.io/tutorials/lora/module-module.html, https://docs.pycom.io/tutorials/all/wlan.html, and https://tools.ietf.org/html/rfc2616#section-4
# Comment style: # for normal comments, ## for theory / personal comments
## Yes, I linked RFC2616, the document for HTTP/1.1. There's no native HTTP implementation.


from network import LoRa, WLAN
import machine
import socket

# Constants
WIFI_SSID = "Lim Zone Portable"
WIFI_PASSWORD = "pyrd7990"
POST_IP = "192.168.43.116"
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
    tcp_s.setblocking(True)
    ok_message = tcp_s.recv(256)
    tcp_s.close()
    return strip_headers(ok_message)

# Discards all the HTTP headers until the body
def strip_headers(data):
    return data.split(b"\r\n")[-1]

# Do work with data
if __name__ == "__main__":
    buf = b''
    while True:
        buf = s.recv(64)

        # Verify the buffer
        if buf.count(b",") != 4:
            continue # we haven't recieved the full buffer

        # Send the buffer
        ok_message = http_post(POST_IP, POST_PORT, buf)

        # Transmit the ok message back to the slave(s) NOTE: Hacky hack hack
        s.send(ok_message)
