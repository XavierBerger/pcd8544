#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcd8544.lcd as lcd
import time, os,sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

try:
  lcd.init()
  lcd.cls()
  lcd.backlight(ON)
  lcd.load_bitmap("raspi.bmp", True)
  time.sleep(10)
except KeyboardInterrupt:
  pass 
finally:
  lcd.cls()
  lcd.backlight(OFF)
