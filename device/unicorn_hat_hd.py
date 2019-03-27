#!/usr/bin/python3

import time
import logging
from device.base_devices import Device

_UnicornHat = None

class UnicornHatHD(Device):
    # this Unicorn hat has the USB port on the right
    def __init__(self, rotate=0):
        if _UnicornHat:
            self.hat = _UnicornHat
            self.width, self.height = _UnicornHat.get_shape()
        else:
            raise RuntimeError("Unicorn Hat display requires the unicornhathd module.")
        Device.__init__(self, rotate)
        self.hat.rotation(self.rotate)

    def display_icon(self, icon, transition=None, clear=False, is_banner=False):
        if clear:
            self.clear()

        if transition:
            for frame in self.current.transition(icon, transition):
                self._display_icon(frame)
                time.sleep(0.05)
        else:
            self._display_icon(icon)

        self.current = icon

        if is_banner:
            time.sleep(0.8)
        else:
            time.sleep(1.5)

    def _display_icon(self, icon):
        for y in range(self.width):
            for x in range(self.height):
                r, g, b = icon.get_pixel(x/self.width,y/self.height)
                self.hat.set_pixel(x,y,r,g,b)
        self.hat.show()

    def clear(self, wait=True):
        self.hat.off()
        if wait:
            time.sleep(0.5)
        self.current = None

    def __exit__(self, *args):
        self.clear(wait=False)

class QuadUnicornHatHD(Device):
    def __init__(self, rotate=0):
        if _UnicornHat:
            self.hat = _UnicornHat
            self.width, self.height = _UnicornHat.get_shape()
            self.icons = [[],[]]
        else:
            raise RuntimeError("Unicorn Hat display requires the unicornhathd module.")
        self.page = 0
        Device.__init__(self, rotate)
        self.hat.rotation(self.rotate)

    def display_icon(self, icon, transition=None, clear=False, is_banner=False):
        if clear or is_banner or len(self.icons[1])>=2:
            self.newline()
            if self.page % 2 == 1:
                self.page += 1

        self.icons[1].append(icon)
        self.refresh()
        self.page += 1

        if self.page == 4:
            time.sleep(1.5)
            self.page = 0
        elif self.page == 2:
            time.sleep(0.2)
        else:
            time.sleep(0.1)

    def clear(self):
        self.icons = [[], []]
        self.page = 0
        self.refresh()

    def newline(self):
        self.icons = [self.icons[1], []]

    def refresh_space(self, xs, ys, icon):
        w = self.width//2
        h = self.height//2
        for y in range(h):
           for x in range(w):
               if icon is None:
                   self.hat.set_pixel(w*xs+x, h*(1-ys)+y, 0, 0, 0)
               else:
                   r, g, b = icon.get_pixel(x/w, y/h)
                   self.hat.set_pixel(w*xs+x, h*(1-ys)+y, r, g, b)

    def refresh(self):
        for xs in range(2):
            for ys in range(2):
                try:
                    r = self.icons[ys]
                except IndexError:
                    self.refresh_space(xs, ys, None)
                    continue
                try:
                    i = r[xs]
                except IndexError:
                    self.refresh_space(xs, ys, None)
                    continue
                self.refresh_space(xs, ys, i)
        self.hat.show()


    def __exit__(self, *args):
        self.hat.off()

try:
    import unicornhathd
    _UnicornHat = unicornhathd # unlike the sense hat the unicorn is just a module
    Device.CHOICES.update({
        "unicornhathd": UnicornHatHD,
        "uhhd": UnicornHatHD,
        "quadunicornhathd": QuadUnicornHatHD,
        "quhhd": QuadUnicornHatHD })
except ImportError:
    pass

