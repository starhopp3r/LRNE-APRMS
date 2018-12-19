# A UART communications tester. Use a MicroPython compatible board to test UART communications with the other board.
# Author: s u d o_

from machine import UART
uart = UART(1, baudrate=9600, bits=8)
uart.write(b"0,16/12/18 11:08,51.174693,-3.061574,11\r\n")

print("Reset the microcontroller to send testing data again.\n")
