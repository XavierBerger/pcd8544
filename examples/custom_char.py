#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcd8544.lcd as lcd
import time
import os
import sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

try:
  lcd.init()
  lcd.cls()
  lcd.backlight(ON)
  # Test a custom character for 0x7f (supposed to be a bell)
  # . . . - - - - -
  # . . . - - X - -
  # . . . - X X X -
  # . . . - X - X -
  # . . . X - - - X
  # . . . X X X X X
  # . . . - - X X -
  # . . . - - - - -
  lcd.define_custom([0x30,0x2c,0x66,0x6c,0x30])
  lcd.text("\x7f \x7f \x7f \x7f \x7f \x7f \x7f ")
  lcd.text("    Hello     ")
  lcd.text(" Raspberry Pi")
  time.sleep(10);
except KeyboardInterrupt:
  pass
finally:
  lcd.cls;
  lcd.backlight(OFF);

