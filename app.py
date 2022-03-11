#!/home/pi/hyaboat-flask/env/bin/python

from pyfirmata import Arduino

from model.detect import main as detect

from arduino.relay import Relay
from l298n import L298N
from arduino.servo import Servo

PORT = "/dev/ttyACM0"
board = Arduino(PORT)

relay = Relay(board, 13)
motor = L298N(board, 11, 7, 6, 12, 8, 10)
servo = Servo(board, 9)

if __name__ == "__main__":
    detect(relay, motor, servo)

#     web.run_app(app, host="192.168.68.121", port="8080")
