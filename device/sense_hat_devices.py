#!/usr/bin/python3

import time
from device.base_devices import Device

_SenseHat = None

class SenseHat(Device):
    # this sense hat has the USB port on the right
    def __init__(self):
        if _SenseHat:
            self.hat = _SenseHat()
        else:
            raise RuntimeError("Sense Hat display requires the sense_hat module.")
        Device.__init__(self)

    def display_icon(self, icon, transition=None, clear=False, is_banner=False):
        if clear:
            self.clear()

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


    def clear(self, wait=True):
        self.hat.clear()
        if wait:
            time.sleep(0.5)
        self.current = None

    def __exit__(self, *args):
        self.clear(wait=False)

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
        "r-sensehat": SenseHat,
        "sensehat": SenseHat,
        "v-sensehat": VerticalSenseHat,
        "l-sensehat": LeftSenseHat })
except ImportError:
    pass

