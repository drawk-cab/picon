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
    def __init__(self):
        SenseHat.__init__(self)
        self.hat.rotation = 90

class UnicornHat(Device):
    def display(self, icon):
        raise NotSupportedError

CHOICES = { "stdout": Device,
            "astropi": SenseHat,
            "sense": SenseHat,
            "v-astropi": VerticalSenseHat,
            "v-sense": VerticalSenseHat,
            "unicorn": UnicornHat }

