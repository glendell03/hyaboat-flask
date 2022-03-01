import pyfirmata


# class Relay:
#     def __init__(self) -> None:
#         self.pin = 13
#         self.board = pyfirmata.Arduino("/dev/ttyACM0")

#     def turnOn(self):
#         self.board.digital[self.pin].write(1)

#     def turnOff(self):
#         self.board.digital[self.pin].write(0)

pin = 13
board = pyfirmata.Arduino("/dev/ttyACM0")

def RelayOn():
    board.digital[pin].write(1)

def RelayOff():
    board.digital[pin].write(0)

