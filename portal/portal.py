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

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

DOOR_STATE_PIN = 13
DOOR_LOCK_STATE_PIN = 15
#CLOSEBUTTON_PIN = 29

BUZZER_PIN = 31
KEYMATIC_CLOSE_PIN = 11
KEYMATIC_OPEN_PIN = 7

#GPIO.setup(CLOSEBUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOOR_STATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOOR_LOCK_STATE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(KEYMATIC_CLOSE_PIN, GPIO.OUT)
GPIO.setup(KEYMATIC_OPEN_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

GPIO.output(KEYMATIC_CLOSE_PIN, 0)
GPIO.output(KEYMATIC_OPEN_PIN, 0)
GPIO.output(BUZZER_PIN, 0)

LOGFILE = '/var/log/portal/portal.log'
LOCKFILE = '/var/run/lock/portal.lock'
STATUSFILE = '/var/log/portal/keyholder'
SERTIMEOUT = 1

LOGLEVEL = 2


class Portal():
    """
    Generic docstring
    """

    def __enter__(self):
        """Generic docstring"""
        return self

    def __exit__(self, type, value, traceback):
        """Generic docstring"""
        # self.serial.__exit__(type, value, traceback)

    def open_portal(self):
        """
        Open the door
        """
        for _ in range(3):
            print("opening keymatic")
            GPIO.output(KEYMATIC_OPEN_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(KEYMATIC_OPEN_PIN, GPIO.LOW)
            time.sleep(5)
            if self.is_reed_open(15):
                self.beep_success()
                return
            self.beep_fail()

    def is_reed_open(self, timeout=0):
        """
        Generic docstring
        """
        status = GPIO.input(DOOR_LOCK_STATE_PIN)
        for _ in range(timeout):
            status = GPIO.input(DOOR_LOCK_STATE_PIN)
            log("door lock status: " + str(status), 2)
            if status:
                return True
            time.sleep(1)
        return status

    def is_reed_closed(self, timeout=0):
        """Generic docstring"""
        status = GPIO.input(DOOR_LOCK_STATE_PIN)
        for _ in range(timeout):
            status = GPIO.input(DOOR_LOCK_STATE_PIN)
            log("door lock status: " + str(status), 2)
            if not status:
                return True
            time.sleep(1)

        return not status

    def is_door_button_open(self):
        """Generic docstring"""
        return GPIO.input(DOOR_STATE_PIN)

    def close_door(self):
        """Generic docstring"""
        log("closing keymatic", 2)
        GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.LOW)

    def close_portal(self):
        """Generic docstring"""
        for _ in range(30):
            self.beep(.5)
            if self.is_door_button_open() == 0:
                log("door closed", 2)
                time.sleep(.5)
                GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(KEYMATIC_CLOSE_PIN, GPIO.LOW)
                if self.is_reed_closed(15):
                    self.beep_success()
                    return
                else:
                    break
            log("door still open", 2)
            time.sleep(0.5)
        self.alarm()

    def alarm(self):
        """
        Generic docstring
        """
        log("door close failed")
        self.beep_alarm()

    def beep(self, duration=0.2):
        """
        Generic docstring
        """
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def beep_alarm(self):
        """
        Generic docstring
        """
        for _ in range(30):
            self.beep(0.1)
            time.sleep(0.1)

    def beep_success(self):
        """
        Generic docstring
        """
        for _ in range(2):
            self.beep(0.2)
            time.sleep(0.2)

    def beep_fail(self):
        """
        Generic docstring
        """
        self.beep(1)


class Lockfile():
    """Generic docstring"""
    def __init__(self, lockfile):
        """Generic docstring"""
        self.lockfile = lockfile
        self.create_lock()

    def __enter__(self):
        """Generic docstring"""
        return self

    def __exit__(self, type, value, traceback):
        """Generic docstring"""
        self.remove_lock()

    def create_lock(self):
        """
        create a lockfile
        """
        if os.path.isfile(LOCKFILE):
            fp = open(self.lockfile, 'r')
            content = fp.read()
            content.strip()
            if self.lockpid_running(content):
                log('Could not lock open job, locked by %s' % content)
                sys.exit(1)
            else:
                log("Removing lockfile as %s isn't running anymore" % content, 2)
                self.remove_lock()
        with open(self.lockfile, 'w') as fp:
            fp.write(str(os.getpid()))

    def remove_lock(self):
        """
        remove the lock file
        """
        try:
            os.remove(self.lockfile)
        except OSError:
            log("Couldn't remove lock file: %s" % self.lockfile)

    def lockpid_running(self, pid):
        """
        check if pid is running
        """
        try:
            os.kill(int(pid), 0)
        except OSError:
            return False
        else:
            return True


def main():
    """Generic docstring"""
    motd()
    parser = get_option_parser()

    options = parser.parse_args()

    with Lockfile(LOCKFILE):
        with Portal() as portal:

            portal.beep(0.1)
            if options.action == 'open':
                msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
                log(msg)
                if options.nick:
                    update_keyholder(options.nick)
                else:
                    name = options.name
                    name = name.split(' ')
                    name[0] = name[0][:3]
                    if len(name) > 1:
                        name[len(name) - 1] = name[1][:1]
                    name = ' '.join(name)
                    update_keyholder(name)
                portal.open_portal()
            if options.action == 'close':
                msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
                log(msg)
                update_keyholder("No Keyholder")
                portal.close_portal()


def motd():
    """Generic docstring"""
    with open('/opt/Portal-v4/portal/motd.txt', 'r') as f:
        for line in f.readlines():
            print(line.rstrip('\n'))


def log(message, level=1):
    """Generic docstring"""
    if level > LOGLEVEL:
        return
    timestamp = datetime.datetime.now()
    message = str(timestamp) + ':\t' + message
    print(message)
    f = open(LOGFILE, 'a')
    f.write(message + "\n")
    f.close()


def check_options(options):
    """Generic docstring"""
    if not options.serial:
        print('Please provide a serial')
        sys.exit(1)
    if not options.name:
        print('Please provide a name')
        sys.exit(1)
    if not options.action:
        print('Please specify a action (open|close)')
        sys.exit(1)

    valid_actions = ['open', 'close']
    if options.action not in valid_actions:
        print('Option must be open or close')
        sys.exit(1)


def update_keyholder(name):
    """
    update the status file with the current keyholder
    """
    with open(STATUSFILE, 'w') as f:
        f.write(name)
        gid = grp.getgrnam("portal").gr_gid
        uid = uid = pwd.getpwnam("open").pw_uid


def get_option_parser():
    """
    create Argument Parser object and add options
    """
    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('-s', '--serial',
                        dest='serial',
                        help='members ID',
                        required=True)
    parser.add_argument('-n', '--name',
                        dest='name',
                        help='keymembers name name_surname',
                        required=True)
    parser.add_argument('--nick',
                        dest='nick',
                        help='OPT: members nickname',
                        required=True)
    parser.add_argument('-a', '--action',
                        dest='action',
                        help='open|close',
                        required=True)
    parser.add_argument('-l', '--last',
                        dest='last',
                        help='OPT: last valid day of the key')
    parser.add_argument('-f', '--first',
                        dest='first',
                        help='OPT: first valid day of the key')
    return parser


if __name__ == '__main__':
    main()

GPIO.cleanup()
