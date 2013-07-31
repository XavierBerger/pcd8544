#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcd8544.lcd as lcd
import time, os, sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

try:
  lcd.init()
  lcd.cls()
  lcd.backlight(ON)
  lcd.centre_text(0,"Raspberry Pi")
  while 1:
     lcd.centre_text(2,time.strftime("%d %b %Y", time.localtime()))
     lcd.centre_text(3,time.strftime("%H:%M:%S", time.localtime()))
     time.sleep(0.25)
except KeyboardInterrupt:
  pass
finally:
  lcd.cls()
  lcd.backlight(OFF)

