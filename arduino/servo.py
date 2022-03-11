from pyfirmata import Arduino, SERVO, util
from time import sleep

class Servo():
    def __init__(self, board, pin):
        self.board = board
        self.pin = pin
        self.servo = self.board.get_pin(f'd:{self.pin}:s')
    
    def angle(self, angle):
        self.servo.write(angle)
        sleep(0.15)

