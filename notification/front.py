from pushbullet import Pushbullet
import RPi.GPIO as GPIO
from time import sleep 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

pb=Pushbullet("o.nLMpYqBfAUNTwOOqe7x1QadFblu5fG0d")
print(pb.devices)

while True:
    i=GPIO.input(11)
    if i==1:
        print("Not Full storage")
        sleep(1)
    elif i==0:
        print("Full Storage")

        dev=pb.get_device('Xiaomi 2201117TG')
        push = dev.push_note("HYABOAT","Alert! Your Trashbin is full")
        sleep(1)

