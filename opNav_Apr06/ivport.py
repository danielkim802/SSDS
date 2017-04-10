#!/usr/bin/env python
#
# This file is part of Ivport.
# Copyright (C) 2016 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# Ivport is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ivport is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#title           :ivport.py
#description     :ivport.py is module for capturing ivport camera multiplexer
#author          :Caner Durmusoglu & Doga Yucalan
#date            :20160514
#version         :0.1
#usage           :import ivport
#notes           :
#python_version  :2.7
#==============================================================================

import sys

try:
    import IIC
    import RPi.GPIO as gp
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)
except:
    print "There are no IIC.py and RPi.GPIO module."
    print "install RPi.GPIO: sudo apt-get install python-rpi.gpio"
    sys.exit(0)

try:
    import picamera
    from picamera.array import PiRGBArray
except:
    print "There are no picamera module or directory."
    sys.exit(0)

TYPE_QUAD = 0
TYPE_QUAD2 = 1
TYPE_DUAL = 2
TYPE_DUAL2 = 3

class IVPort():
    IVJP = {'A': (11, 12), 'C': (21, 22), 'B': (15, 16), 'D': (23, 24)}
    pins = list(reduce(lambda x,y: x+y, IVJP.values()))
    pins.sort()
    DIVJP = {i+1 : x for i,x in enumerate(pins)}
    del(pins)
    
    def __init__(self, iv_type=TYPE_DUAL2, iv_jumper=1):

        self.fPin = self.f1Pin = self.f2Pin = self.ePin = 0
        self.ivport_type = iv_type
        self.is_camera_v2 = self.ivport_type in (TYPE_DUAL2, TYPE_QUAD2)
        self.is_dual = self.ivport_type in (TYPE_DUAL2, TYPE_DUAL)
        self.ivport_jumper = iv_jumper
        if not self.is_dual: self.ivport_jumper = 'A'
        self.camera = 1
        self.is_opened = False

        if self.is_camera_v2:
            self.iviic = IIC.IIC(addr=(0x70), bus_enable =(0x01))

        self.link_gpio()

    def link_gpio(self):
        if self.is_dual:
            self.fPin = self.DIVJP[self.ivport_jumper]
            gp.setup(self.fPin, gp.OUT)
        else:
            self.f1Pin, self.f2Pin = self.IVJP[self.ivport_jumper]
            self.ePin = 7
            gp.setup(self.f1Pin, gp.OUT)
            gp.setup(self.f2Pin, gp.OUT)
            gp.setup(self.ePin, gp.OUT)

    # ivport camera change
    def camera_change(self, camera=1):
        if self.is_dual:
            if camera == 1:
                if self.is_camera_v2: self.iviic.write_control_register((0x01))
                gp.output(self.fPin, False)
            elif camera == 2:
                if self.is_camera_v2: self.iviic.write_control_register((0x02))
                gp.output(self.fPin, True)
            else:
                print "Ivport type is DUAL."
                print "There isnt camera: %d" % camera
                self.close()
                sys.exit(0)
        else:
            if camera == 1:
                if self.is_camera_v2: self.iviic.write_control_register((0x01))
                gp.output(self.ePin, False)
                gp.output(self.f1Pin, False)
                gp.output(self.f2Pin, True)
            elif camera == 2:
                if self.is_camera_v2: self.iviic.write_control_register((0x02))
                gp.output(self.ePin, True)
                gp.output(self.f1Pin, False)
                gp.output(self.f2Pin, True)
            elif camera == 3:
                if self.is_camera_v2: self.iviic.write_control_register((0x04))
                gp.output(self.ePin, False)
                gp.output(self.f1Pin, True)
                gp.output(self.f2Pin, False)
            elif camera == 4:
                if self.is_camera_v2: self.iviic.write_control_register((0x08))
                gp.output(self.ePin, True)
                gp.output(self.f1Pin, True)
                gp.output(self.f2Pin, False)
            else:
                print "Ivport type is QUAD."
                print "Cluster feature hasnt been implemented yet."
                print "There isnt camera: %d" % camera
                self.close()
                sys.exit(0)
        self.camera = camera

    # picamera initialize
    def camera_open(self, resolution=None, framerate=None, sensor_mode=0, camera_v2=False):
        if self.is_opened: return
        self.picam = picamera.PiCamera(resolution=resolution, framerate=framerate, sensor_mode=sensor_mode, camera_v2=camera_v2)
        #rawCapture = PiRGBArray(self.picam, size=resolution)
        self.is_opened = True
        #return rawCapture
        
