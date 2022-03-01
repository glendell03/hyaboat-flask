import RPI.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.board)

GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 50)

pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.changeDutyCycle(0)

SetAngle(90)

pwm.stop()
GPIO.cleanup()