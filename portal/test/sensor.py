#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BOARD)

status = 'closed'

DOOR_LOCK_STATE_PIN = 15
DOOR_STATE_PIN = 13

GPIO.setup(DOOR_LOCK_STATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(DOOR_LOCK_STATE_PIN, GPIO.IN)
GPIO.setup(DOOR_STATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


print(GPIO.input(DOOR_LOCK_STATE_PIN))

#if GPIO.input(DOOR_LOCK_STATE_PIN) == 1:
if GPIO.input(DOOR_LOCK_STATE_PIN):
    status = 'open'
else:
    status = 'closed'


print(status)

try:
    while True:
        print("lock " + str(GPIO.input(DOOR_LOCK_STATE_PIN)))
        print("reed " + str(GPIO.input(DOOR_STATE_PIN)))
        if GPIO.input(DOOR_LOCK_STATE_PIN):
            print('open')
        else:
            print('closed')

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
