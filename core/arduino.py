import serial
import time

def entrada():
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
    arduino.write(b'H')
    time.sleep(5)
    arduino.write(b'L')
    time.sleep(5)
    arduino.close()

