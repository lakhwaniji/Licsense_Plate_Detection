from pyfirmata import Arduino, SERVO, util
from time import sleep
port = '/dev/cu.usbmodem11101'
pin=10
board=Arduino (port)
board.digital [pin].mode=SERVO
def rotateservo(pin, angle) :
    board.digital[pin].write(angle)
    sleep (0.015)

def open():
    for i in range (180,90,-1) :
        rotateservo(pin, i)

def close():
    for i in range (90,180) :
        rotateservo(pin, i)

close()