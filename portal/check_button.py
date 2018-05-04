#!/usr/bin/env python3

import subprocess
import datetime

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

GPIO.cleanup()

CLOSEBUTTON_PIN = 29

GPIO.setup(CLOSEBUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pushed(channel):
    print(str(datetime.datetime.now()) + ": door close requested by button")
    subprocess.call(["/opt/Portal-v4/portal/portal.py",
                     "-a", "close",
                     "-s", "0000",
                     "--nick", "\"CloseButton\"",
                     "-n", "\"CloseButton\"",
                     "-l", "2023-04-02",
                     "-f", "2015-04-25"])

GPIO.add_event_detect(CLOSEBUTTON_PIN, GPIO.RISING, callback=button_pushed, bouncetime=1000)

try:
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
