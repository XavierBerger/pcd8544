#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PIL import Image,ImageDraw,ImageFont
import pcd8544.lcd as lcd
import os
import sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

try:
    lcd.init()
    lcd.cls()
    lcd.backlight(ON)
    for i in xrange(32, 116):
        lcd.display_char(chr(i))
    time.sleep(10)
except KeyboardInterrupt:
  pass
finally:
  lcd.cls;
  lcd.backlight(OFF);

