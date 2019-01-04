# A standard-to-standard compliant UART testing script
# Author: s u d o_

from machine import UART, Pin
uart = UART(1, baudrate=9600, bits=8, pins=("P3", "P4"))

previous_data = b"#0,Test Broadcast,P#"

# There are 2 kinds of messages to read: "ready" and the actual message.
## This allows me to save the need to store unneeded state
while True:
    data = uart.read()
   
    if data == None:
        continue
    elif data.startswith("OK"): # ready message, respond with previous data
        print("ok msg from uart")
        uart.write(previous_data)
    elif not data == b"": # normal operation
        if data[0] == 35 and data[-1] == 35 and data.count(b",") == 5:
            exploded_data = data[1:-1].decode().split(',')
            if exploded_data[-1] == '1':
                print("Should turn off the screen now") # TODO: Turn off screen

            compass_data = ",".join(exploded_data[:-1])
            print("Compass data: %s" % (compass_data))

        # TODO: Recieve some form of response, for now:
        response = b"#lavis la li da\nP#"
        exploded_response = response[1:-1].decode().split('\n')
        previous_data = "#0,%s,%s#" % (exploded_response[0], exploded_response[1]) 
        print("to uart: %s" % (previous_data))
        uart.write(previous_data)
