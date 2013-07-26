#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcd8544.lcd as lcd
import os, sys

ON, OFF = [1, 0]

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

lcd.init()
lcd.cls()
