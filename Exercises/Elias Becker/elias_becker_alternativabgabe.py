from time import sleep
import datetime
import serial
import os
import math
try:
    import RPi.GPIO as GPIO
    from picamera import PiCamera
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# region setup

# region RPI setup
buttonPin = 21
WorkingLedPin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(WorkingLedPin, GPIO.IN, initial=GPIO.LOW)
# endregion

# region serial arduino setup
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()
# endregion

# region stepper setup

#The Stepper Motor 17HS4401S does 200 Steps per Rotation, therefore stepperSteps ~ ImagesToShoot
stepperSteps = 10
imagesToShoot = int(math.ceil(200/stepperSteps))
# endregion

# endregion
def startScan():
    print("initializing scan...")
    GPIO.output(WorkingLedPin, GPIO.HIGH)
    now = datetime.datetime.now()
    os.mkdir(now.year + "-" + now.month + "-" + now.day + "-" + now.hour + "-" + now.minute + "-" + now.second)
    camera = PiCamera()
    for i in range(imagesToShoot+1):
        ser.write("next")
        sleep(1)
        camera.capture('now.year + "-" + now.month + "-" + now.day + "-" + now.hour + "-" + now.minute + "-" + now.second/image' + i + ".jpg")
        sleep(1)
    print("scan finished")
    GPIO.output(WorkingLedPin, GPIO.LOW)

while True:
    if GPIO.input(buttonPin):
        startScan()