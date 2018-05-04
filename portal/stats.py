#!/usr/bin/env python3

import time
from datetime import date
import sys


PORTALLOG = "/var/log/portal/portal.log"

AUTHORIZED_KEYS = "/home/open/.ssh/authorized_keys"

keyholders = []

today = date.today()

two_years_ago = str(today.year-2) + "-01-01"

print(two_years_ago)
print(date.today())


file = open(AUTHORIZED_KEYS, "r")
for line in file:
	if "open -s " in line:
		line2 = line.split(" ",9)
		line3 = line.split("\\\"",4)
		print(line2[4])
		print(line3[3])

file = open(PORTALLOG, "r")
for line in file:
	if "ID:" in line:
		line2 = line.split(" ",1)
		if line2[0] > two_years_ago:
			# print(line2[1])
			keyholder = line2[1].split("by: ",1)
			keyholder2 = keyholder[1].split(" (ID: ",2)
			# print(keyholder[1].rstrip())
			print(keyholder2[0].rstrip())
			print(keyholder2[1].rstrip(")\n"))
		else:
			pass
	else:
		pass

file.close
