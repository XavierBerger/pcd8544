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
  if ( lcd.LED != 1 ):
      sys.exit('LED pin should be GPIO1 (12)')
  # Backlight PWM testing -- off -> 25% -> off
  for i in range(0,1023,16):
      lcd.set_brightness(i)
      time.sleep(0.025)
  for i in range(1023,0,-16):
      lcd.set_brightness(i)
      time.sleep(0.025)
except KeyboardInterrupt:
  pass
finally:
  lcd.cls()
  lcd.backlight(OFF)

