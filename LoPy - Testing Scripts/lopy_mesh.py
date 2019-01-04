# Basic mesh script
# Author: s u d o _
# Reference: https://github.com/pycom/pycom-libraries/blob/master/lib/lora_mesh/main.py
from network import LoRa
import socket
import time
import utime
import ubinascii
import pycom
import machine

from loramesh import Loramesh

lora = LoRa(mode=LoRa.LORA, region=LoRa.US915, frequency=902000001)
MAC = str(ubinascii.hexlify(lora.mac()))[2:-1]

mesh = Loramesh(lora)

while True:
    print("%d: State %s, single %s" % (time.time(), mesh.cli('state'), mesh.cli('singleton')))
    time.sleep(2)
    if not mesh.is_connected():
        continue

    neighbours = mesh.neighbors_ip()
    if len(neighbours) == 0:
        print('No neigbours')
        continue

    print('Neighbours found: %s' % neighbours)
    break

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
myport = 1234
s.bind(myport)
pack_num = 1
msg = "Hello World! MAC: " + MAC + ", pack: "
ip = mesh.ip()

while True:
    print("%d: State %s, single %s, IP %s" % (time.time(), mesh.cli("state"), mesh.cli("singleton"), mesh.ip()))
    
    new_ip = mesh.ip()
    if ip != new_ip:
        print("IP changed from: %s to %s" % (ip, new_ip))
        ip = new_ip

    rcv_data, rcv_addr = s.recvfrom(128)
    if len(rcv_data) > 0:
        rcv_ip, rcv_port = rcv_addr
        print("Incoming %d bytes from %s (port %d)" % (len(rcv_data), rcv_ip, rcv_port))
        print(rcv_data)

        if rcv_data.startswith("Hello"):
            try:
                s.sendto('ACK ' + MAC + ' ' + str(rcv_data)[2:-1], (rcv_ip, rcv_port))
            except Exception:
                pass
        continue

    neighbours = mesh.neighbors_ip()
    print("%d Neighbours %s" % (len(neighbours), neighbours))

    for neighbour in neighbours:
        if mesh.ping(neighbour) > 0:
            print("Ping OK from neighbour %s" % neighbour)
        else:
            print("Ping not recieved from neighbour %s" % neighbour)
    
        time.sleep(10)
    
        pack_num = pack_num + 1
        try:
            s.sendto(msg + str(pack_num), (neighbour, myport))
            print('Sent message to %s' % (neighbour))
        except Exception:
            pass
    
#        time.sleep(20 + machine.rng() % 20)
#    
#    time.sleep(30 + machine.rng() % 30)
