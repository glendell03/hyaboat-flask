from pyfirmata import Arduino
from l298n import L298N


def main():
    PORT = "/dev/ttyACM0"
    board = Arduino(PORT)

    motor = L298N(board, 11, 7, 6, 12,8,10)

    motor.forward(0.5, 0.5)
    # motor.full_stop(1)

if __name__ == "__main__":
    main()