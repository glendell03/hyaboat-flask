import pyfirmata
from time import sleep

class Relay:
     def __init__(self, board, pin):
         self.pin = pin
         self.board = board

         self.mod = self.board.get_pin(f'd:{self.pin}:o')

     def turnOn(self):
         self.mod.write(1)
         sleep(0.15)

     def turnOff(self):
         self.mod.write(0)
         sleep(0.15)

