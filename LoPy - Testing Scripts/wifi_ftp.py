# Preload this script onto the LoPy for easier WiFi access to the lopy
# Author: s u d o _

from network import WLAN, Server
import machine

wlan = WLAN(mode=WLAN.STA)

while True:
    for network in wlan.scan():
        if network[0] == "<wifi ssid here>":
            wlan.connect(network[0], auth=(network[2], "<wifi password here>"))
            while wlan.isconnected() == False:
                machine.idle()
            break

    if wlan.isconnected():
        break

server = Server(login=("user", "password"), timeout=300)
while server.isrunning() == False:
    machine.idle()
