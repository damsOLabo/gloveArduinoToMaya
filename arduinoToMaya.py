# Python module external to Maya

import socket
import serial

ARDUINO =  "/dev/tty.usbmodem141201"
port_id = 7777
host_adress = "127.0.0.1"

def main():
    maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    maya.connect((host_adress, port_id))
    ser =  serial.Serial(ARDUINO, timeout=1)
    prevVal = None

    while 1:
        # Read the serial value
        ser.flushInput()

        serialValue = ser.readline().strip()

        # Catch any bad serial data:
        try:
            if serialValue != prevVal:
                # Print the value if it differs from the prevVal:
                maya.send(str(serialValue))
                prevVal = serialValue
        except ValueError:
            pass

if __name__ == '__main__':
    main()
