#!/usr/bin/python3

import time
from device.base_devices import Device

_SenseHat = None

class SenseHat(Device):
    def __init__(self, rotate=0):
        if _SenseHat:
            self.hat = _SenseHat()
        else:
            raise RuntimeError("Sense Hat display requires the sense_hat module.")
        Device.__init__(self, rotate)
        self.hat.rotation = rotate

    def display_icon(self, icon, transition=None):
        if transition:
            for frame in self.current.transition(icon, transition):
                self.hat.set_pixels(frame.get_pixels())
                time.sleep(0.05)
        else:
            self.hat.set_pixels(icon.get_pixels())
        self.current = icon

        if is_banner:
            time.sleep(0.8)
        else:
            time.sleep(1.5)


    def clear(self):
        self.hat.clear()
        self.current = None

    def __exit__(self, *args):
        self.clear()

try:
    from sense_hat import SenseHat as _SenseHat
    Device.CHOICES.update({
        "astropi": SenseHat,
        "sensehat": SenseHat })
except ImportError:
    pass

