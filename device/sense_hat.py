#!/usr/bin/python3

from . import *
import time

class SenseHat(Device):
    # this sense hat has the USB port on the right
    def __init__(self):
        if _SenseHat:
            self.hat = _SenseHat()
        else:
            raise NotSupportedError("Sense Hat display requires the sense_hat module.")
        Device.__init__(self)

    def display(self, icon, transition=None):
        if transition=="wipe":
            for frame in self.current.wipe(icon):
                self.hat.set_pixels(frame.get_pixels())
                time.sleep(0.1)
        else:
            self.hat.set_pixels(icon.get_pixels())
        self.current = icon


    def clear(self):
        self.hat.clear()
        self.current = None

    def __exit__(self, *args):
        self.clear()

class VerticalSenseHat(SenseHat):
    # this sense hat has the USB port on the top
    def __init__(self):
        SenseHat.__init__(self)
        self.hat.rotation = 90

class LeftSenseHat(SenseHat):
    # this sense hat has the USB port on the left
    def __init__(self):
        SenseHat.__init__(self)
        self.hat.rotation = 180

try:
    from sense_hat import SenseHat as _SenseHat
    Device.CHOICES.update({
            "astropi": SenseHat,
            "sense": SenseHat,
            "v-sense": VerticalSenseHat,
            "l-sense": LeftSenseHat })
except ImportError:
    _SenseHat = None

