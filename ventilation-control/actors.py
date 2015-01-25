#!/usr/local/bin/python
# coding: utf-8

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

class Actor:
    name = "Actor-with-no-name"

    def setPowerOn(self, on):
        raise NotImplementedError( "Should have implemented this" )

    def is_on(self):
        raise NotImplementedError( "Should have implemented this" )        

class DemoActor(Actor):
    def __init__(self, name):
        self.name = name

    def setPowerOn(self, on):
        print( "Switching actor %s to %r" % (self.name, on) )

    def is_on(self):
        return True

class PaspberrypiActor(Actor):
    pin = -1

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def setPowerOn(self, on):
        GPIO.output(self.pin, on)

    def is_on(self):
        return GPIO.input(self.pin)
