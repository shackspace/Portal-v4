#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import sys
import os
import grp
import pwd
import datetime
import argparse

import RPi.GPIO as GPIO

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

KEYMATIC_CLOSE_PIN = 11
KEYMATIC_OPEN_PIN = 7

GPIO.setup(KEYMATIC_CLOSE_PIN, GPIO.OUT)
GPIO.setup(KEYMATIC_OPEN_PIN, GPIO.OUT)

GPIO.output(KEYMATIC_CLOSE_PIN, 0)
GPIO.output(KEYMATIC_OPEN_PIN, 0)


print("Schliessen")
time.sleep(.5)
GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.HIGH)
GPIO.output(KEYMATIC_OPEN_PIN, GPIO.HIGH)
time.sleep(1)
GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.LOW)
GPIO.output(KEYMATIC_OPEN_PIN, GPIO.LOW)


GPIO.cleanup()
