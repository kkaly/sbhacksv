import serial
import struct
import time

def writeVal(inputVal):
    arduino = serial.Serial('/dev/ttyACM1', 115200, timeout = 0.5)
    #arduino.write(struct.pack("B", 4))
    arduino.write(str(inputVal).encode())

def test():
    for i in reversed(range(2, 6)):
        writeVal(i)
        time.sleep(0.3)

    for i in range(13, 17):
        writeVal(i)
        time.sleep(0.3)


    for i in reversed(range(6, 9)):
        writeVal(i)
        time.sleep(0.3)

    for i in range(17, 20):
        writeVal(i)
        time.sleep(0.3)

    for i in range(9, 13):
        writeVal(i)
        time.sleep(0.3)

    for i in reversed(range(20, 24)):
        writeVal(i)
        time.sleep(0.3)
