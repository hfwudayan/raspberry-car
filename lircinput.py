#!/usr/bin/env python
#https://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python

import pylirc
import RPi.GPIO as GPIO
import threading
import sys
import time

blocking = 0;

class KeyPress(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._char = None
        self._quitKey = None
        self._handlersMap = {}

    def registerHandlers(self,hMap):
        self._handlersMap = hMap;

    def registerQuitKey(self,char):
        self._quitKey = char

    def run(self):
        GPIO.setmode(GPIO.BCM)
        #pylirc.init("pylirc","./irc_conf",blocking)
        pylirc.init("pylirc","./irc_conf")
        allow = pylirc.blocking(0)
        while True:
            time.sleep(1)
            s = pylirc.nextcode()

            while(s):
               time.sleep(1)
               for (code) in s:
                   #print 'Command: ',code["config"]
                   print 'CommandS: ',s
                   lirchar = s[0]
                   print 'Command1:',lirchar
                   self._char = lirchar
                   if self._char == self._quitKey:
                       pylirc.exit()
                       print "QUIT!"
                       return
                   if self._char in self._handlersMap:
                       self._handlersMap[self._char]()

               if(not blocking):
                   s = pylirc.nextcode()
               else:
                   s = []

