#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
import pcd8544.lcd as lcd
import time, os, sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

try:
  lcd.init()
  lcd.cls()
  lcd.backlight(ON)
  ## Generate an image with PIL and put on the display
  # load an available True Type font
  font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 14)

  # New b-w image
  im = Image.new('1', (84,48))
  # New drawable on image
  draw = ImageDraw.Draw(im)
  # Full screen and half-screen ellipses
  draw.ellipse((0,0,im.size[0]-1,im.size[1]-1), outline=1)
  draw.ellipse((im.size[0]/4,im.size[1]/4,im.size[0]/4*3-1,im.size[1]/4*3-1), outline=1)
  # Some simple text for a test (first with TT font, second with default
  draw.text((10,10), "hello", font=font, fill=1)
  draw.text((10,24), "world", fill=1)
  # Check what happens when text exceeds width (clipped)
  draw.text((0,0), "ABCabcDEFdefGHIghi", fill=1)
  # Copy it to the display
  lcd.show_image(im)
  # clean up
  del draw
  del im
  time.sleep(10)
except KeyboardInterrupt:
  pass
finally:
  lcd.cls()
  lcd.backlight(OFF)

