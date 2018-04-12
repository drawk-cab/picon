#!/usr/bin/python3

import time
from device.base_devices import Device

_UnicornHat = None

class UnicornHatHD(Device):
    # this Unicorn hat has the USB port on the right
    def __init__(self):
        if _UnicornHat:
            self.hat = _UnicornHat
            self.width, self.height = _UnicornHat.get_shape()
        else:
            raise RuntimeError("Unicorn Hat display requires the unicornhathd module.")
        Device.__init__(self)

    def display(self, icon, transition=None):
        if transition:
            for frame in self.current.transition(icon, transition):
                self.display(frame)
                time.sleep(0.05)
        else:
            for y in range(self.width):
                for x in range(self.height):
                    r, g, b = icon.get_pixel(x/self.width,y/self.height)
                    self.hat.set_pixel(x,y,r,g,b)
            self.hat.show()
        self.current = icon


    def clear(self):
        self.hat.off()
        self.current = None

    def __exit__(self, *args):
        self.clear()

class VerticalUnicornHatHD(UnicornHatHD):
    # this Unicorn hat has the USB port on the top
    def __init__(self):
        UnicornHatHD.__init__(self)
        self.hat.rotation(270)

class LeftUnicornHatHD(UnicornHatHD):
    # this Unicorn hat has the USB port on the left
    def __init__(self):
        UnicornHatHD.__init__(self)
        self.hat.rotation(180)

try:
    import unicornhathd
    _UnicornHat = unicornhathd # unlike the sense hat the unicorn is just a module
    Device.CHOICES.update({
        "unicornhd": UnicornHatHD,
        "v-unicornhd": VerticalUnicornHatHD,
        "l-unicornhd": LeftUnicornHatHD })
except ImportError:
    pass

