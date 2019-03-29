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

    def post_section(self):
        time.sleep(0.3)

    def post_banner(self, item=None):
        time.sleep(0.3)

    def post_icon(self):
        time.sleep(0.5)

    def display_icon(self, icon, transition=None):
        if transition:
            for frame in self.current.transition(icon, transition):
                self._display_icon(frame)
                time.sleep(0.05)
        else:
            self._display_icon(icon)

        self.current = icon

    def _display_icon(self, icon):
        if icon is None:
            return
        for y in range(self.width):
            for x in range(self.height):
                r, g, b = icon.get_pixel(x/self.width,y/self.height)
                self.hat.set_pixel(x,y,r,g,b)
        self.hat.show()

    def clear(self, wait=True):
        self.hat.off()
        self.current = None

    def __exit__(self, *args):
        self.clear()

class QuadUnicornHatHD(Device):
    def __init__(self, rotate=0):
        if _UnicornHat:
            self.hat = _UnicornHat
            self.width, self.height = _UnicornHat.get_shape()
            self.icons = [[],[]]
        else:
            raise RuntimeError("Unicorn Hat display requires the unicornhathd module.")
        Device.__init__(self, rotate)
        self.hat.rotation(self.rotate)

    def __len__(self):
        return sum(len(x) for x in self.icons)

    def pre_section(self):
        pass

    def post_section(self):
        time.sleep(0.3)

    def pre_banner(self):
        time.sleep(0.4)
        if len(self.icons[1])<2:
            self.newline()

    def post_banner(self, item=None):
        if getattr(item,'icons'):
            if len(item.icons)==2:
                time.sleep(0.3)
                self.newline() # put 2 icons together on the lower line rather than splitting them

    def pre_icon(self):
        pass

    def post_icon(self):
        time.sleep(0.15)

    def display_icon(self, icon, transition=None):
        if len(self.icons[1])==2:
            self.newline()
        self.icons[1].append(icon)
        self.refresh()

    def clear(self):
        for i in range(2):
            self.newline()
        self.page = 0

    def newline(self):
        self.icons = [self.icons[1], []]
        self.refresh()

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

