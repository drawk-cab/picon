#!/usr/bin/python3

try:
    from sense_hat import SenseHat as _SenseHat
except ImportError:
    SenseHat = None

class Device:
    def display(self, icon):
        print(icon)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass 

class SenseHat(Device):
    # this sense hat has the USB port on the right
    def __init__(self):
        if _SenseHat:
            self.hat = _SenseHat()
        else:
            raise NotSupportedError("Sense Hat display requires the sense_hat module.")

    def display(self, icon):
        self.hat.set_pixels(icon.get_pixels())

    def __exit__(self, *args):
        self.hat.clear()

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

class UnicornHat(Device):
    def display(self, icon):
        raise NotSupportedError

CHOICES = { "stdout": Device,
            "astropi": SenseHat,
            "sense": SenseHat,
            "v-sense": VerticalSenseHat,
            "l-sense": LeftSenseHat,
            "unicorn": UnicornHat }

