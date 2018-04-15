#!/usr/bin/python3

import time
import logging

class Device:
    CHOICES = {}

    def __init__(self, rotate=0):
        self.current = None
        self.rotate = ((rotate // 90) * 90) % 360

    def display(self, item, transition=None, clear=True):
        '''Take an Icon, an iterable of Icons, a Report, or something similar, and display it.'''

        try:
            if item.banner:
                self.display_icon(item.banner, clear=clear, is_banner=True)
            elif clear:
                self.clear() # Has banner attribute but value is zero
            clear = False
        except AttributeError:
            pass

        try:
            for icon in item:
                self.display(icon, transition=transition, clear=clear)
                clear = False
        except TypeError:
            self.display_icon(item, transition=transition, clear=clear)
            clear = False

    def display_icon(self, icon, transition=None, clear=False, is_banner=False):
        if clear:
            self.clear()

        if transition:
            print("Transition: %s\n" % transition)
            print(self.current.transition(icon, transition))

        print(icon)
        self.current = icon

        if is_banner:
            time.sleep(0.4)
        else:
            time.sleep(0.8)

    def clear(self):
        print("========================\n")

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass 

Device.CHOICES["stdout"] = Device


