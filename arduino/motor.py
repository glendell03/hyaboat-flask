from pyfirmata import Arduino
from arduino.l298n import L298N


def main():
    PORT = "/dev/ttyACM0"
    board = Arduino(PORT)

    motor = L298N(board, 10, 7, 6)

    motor.forward(0.5, 0.1)

if __name__ == "__main__":
    main()