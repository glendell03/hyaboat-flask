from pyfirmata import Arduino
from time import sleep
import cv2

from model.detect import main as detect
from arduino.relay import Relay
from l298n import L298N
from arduino.servo import Servo

PORT = "/dev/ttyACM0"
board = Arduino(PORT)

def main():
    relay = Relay(board, 13)
    motor = L298N(board, 11,7,6,12,8,10)
    servo = Servo(board, 9)

    detect(relay, motor)


if __name__ == "__main__":
    main()
