#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Code picked up Raspberry Pi forums  
# http://www.raspberrypi.org/phpBB3/viewtopic.php?p=301522#p301522
#
import time
import wiringpi2 as wiringpi
import spidev
from PIL import Image,ImageDraw,ImageFont
from pcd8544.font import FONT

# White backlight
CONTRAST = 0xaa

ROWS = 6
COLUMNS = 14
PIXELS_PER_ROW = 6
ON = 1
OFF = 0

#gpio's :
DC   = 4 # gpio pin 16 = wiringpi no. 4 (BCM 23)
RST  = 5 # gpio pin 18 = wiringpi no. 5 (BCM 24)
LED  = 1 # gpio pin 12 = wiringpi no. 1 (BCM 18)

# SPI connection
SCE  = 10 # gpio pin 24 = wiringpi no. 10 (CE0 BCM 8) 
SCLK = 14 # gpio pin 23 = wiringpi no. 14 (SCLK BCM 11)
DIN  = 12 # gpio pin 19 = wiringpi no. 12 (MOSI BCM 10)


CLSBUF=[0]*(ROWS * COLUMNS * PIXELS_PER_ROW)

ORIGINAL_CUSTOM = FONT['\x7f']

def bit_reverse(value, width=8):
  result = 0
  for _ in xrange(width):
    result = (result << 1) | (value & 1)
    value >>= 1

  return result

BITREVERSE = map(bit_reverse, xrange(256))

spi = spidev.SpiDev()

def init(dev=(0,0),speed=4000000, brightness=256, contrast=CONTRAST):
    spi.open(dev[0],dev[1])
    spi.max_speed_hz=speed

    # Set pin directions.
    wiringpi.wiringPiSetup()
    for pin in [DC, RST]:
        wiringpi.pinMode(pin, 1)

    # Toggle RST low to reset.
    wiringpi.digitalWrite(RST, OFF)
    time.sleep(0.100)
    wiringpi.digitalWrite(RST, ON)
    # Extended mode, bias, vop, basic mode, non-inverted display.
    set_contrast(contrast)

    # if LED == 1 set pin mode to PWM else set it to OUT
    if LED == 1:
        wiringpi.pinMode(LED, 2)
        wiringpi.pwmWrite(LED,0)
    else:
        wiringpi.pinMode(LED, 1)
        wiringpi.digitalWrite(LED, OFF)
 


def lcd_cmd(value):
    wiringpi.digitalWrite(DC, OFF)
    spi.writebytes([value])


def lcd_data(value):
    wiringpi.digitalWrite(DC, ON)
    spi.writebytes([value])


def cls():
    gotoxy(0, 0)
    wiringpi.digitalWrite(DC, ON)
    spi.writebytes(CLSBUF)


def backlight(value):
    set_brightness(256*value)


def set_brightness(led_value):
    if  LED == 1:
        if (0 <= led_value < 1023):
            wiringpi.pwmWrite(LED,led_value)
    else:
        if led_value == 0:
            wiringpi.digitalWrite(LED, OFF)
        else:
            wiringpi.digitalWrite(LED, ON)


def set_contrast(contrast):
    if ( 0x80 <= contrast < 0xFF):
        wiringpi.digitalWrite(DC, OFF)
        spi.writebytes([0x21, 0x14, contrast, 0x20, 0x0c])


def gotoxy(x, y):
    if ( (0 <= x < COLUMNS) and (0 <= y < ROWS)):
        wiringpi.digitalWrite(DC, OFF)
        spi.writebytes([x+128,y+64])


def gotorc(r, c):
    gotoxy(c*6,r)


def text(string, font=FONT):
    for char in string:
        display_char(char, font)


def centre_text(r, word):
    gotorc(r, max(0, (COLUMNS - len(word)) // 2))
    text(word)


def show_custom_char(font=FONT):
    display_char('\x7f', font)


def define_custom_char(values):
    FONT['\x7f'] = values


def restore_custom_char():
    define_custom_char(ORIGINAL_CUSTOM)


def alt_custom_char():
    define_custom_char([0x00, 0x50, 0x3C, 0x52, 0x44])


def pi_custom_char():
    define_custom_char([0x19, 0x25, 0x5A, 0x25, 0x19])


def display_char(char, font=FONT):
    try:
        wiringpi.digitalWrite(DC, ON)
        spi.writebytes(font[char]+[0])

    except KeyError:
        pass # Ignore undefined characters.


def load_bitmap(filename, reverse=False):
    mask = 0x00 if reverse else 0xff
    gotoxy(0, 0)
    with open(filename, 'rb') as bitmap_file:
        for x in xrange(6):
          for y in xrange(84):
            bitmap_file.seek(0x3e + y * 8 + x)
            lcd_data(BITREVERSE[ord(bitmap_file.read(1))] ^ mask)


def show_image(im):
    # Rotate and mirror the image
    rim = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)

    # Change display to vertical write mode for graphics
    wiringpi.digitalWrite(DC, OFF)
    spi.writebytes([0x22])

    # Start at upper left corner
    gotoxy(0, 0)
    # Put on display with reversed bit order
    wiringpi.digitalWrite(DC, ON)
    spi.writebytes( [ BITREVERSE[ord(x)] for x in list(rim.tostring()) ] )

    # Switch back to horizontal write mode for text
    wiringpi.digitalWrite(DC, OFF)
    spi.writebytes([0x20])

