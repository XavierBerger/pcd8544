#!/usr/bin/env python

from distutils.core import setup
setup(
    name = "pcd8544",
    version = "0.1.0",
    author = "Xavier Berger and Raspberry Pi community",
    author_email = "berger.xavier@gmail.com",
    description = ("A small library to drive the PCD8544 LCD using WiringPi software bit-banding"),
    license = "GPLv3",
    keywords = "raspberry pi rpi pcd 8544 lcd nokiai 3310 5110",
    url = "https://github.com/XavierBerger/pcd8544",
    packages=['pcd8544'],
    package_dir={'pcd8544': 'src'}
)
