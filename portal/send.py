#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import simplejson as json
import urllib3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

keyholder = open('/var/log/portal/keyholder', 'r')
keyholder = keyholder.readline()
keyholder = keyholder.rstrip('\n')

status = 'closed'

URL = 'http://10.0.2.10:8080/push'
DOOR_LOCK_STATE_PIN = 15

GPIO.setup(DOOR_LOCK_STATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if GPIO.input(DOOR_LOCK_STATE_PIN):
    status = 'open'
else:
    status = 'closed'

encoded_body = json.dumps({
    "status": status,
    "keyholder": keyholder})

http = urllib3.PoolManager()

r = http.request('POST', URL,
                 headers={'Content-Type': 'application/json'},
                 body=encoded_body)
