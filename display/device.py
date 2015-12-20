#!/usr/bin/python3

class Device:
    def display(icon):
        print(icon)

class AstroPiHat(Device):
    def display(icon):
        raise NotSupportedError

class UnicornHat(Device):
    def display(icon):
        raise NotSupportedError

CHOICES = { "stdout": Device,
            "astropi": AstroPiHat,
            "unicorn": UnicornHat }

