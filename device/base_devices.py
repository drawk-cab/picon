#!/usr/bin/python3

import time
import logging

class Device:
    CHOICES = {}

    def __init__(self, rotate=0):
        self.current = None
        # Most devices support rotation, make it easy
        self.rotate = ((rotate // 90) * 90) % 360

    def pre_section(self):
        pass

    def post_section(self):
        pass

    def display_section(self, item, transition=None):
        '''Display an Icon or Report, or an iterable of these, as a section which should be kept together.'''
        self.pre_section()
        self.display(item, transition)
        self.post_section()

    def pre_banner(self):
        pass

    def post_banner(self, item=None):
        pass

    def pre_icon(self):
        pass

    def post_icon(self):
        pass

    def display(self, item, transition=None):
        '''Take an Icon, an iterable of Icons, a Report, or something similar, and display it.'''
        if hasattr(item,'banner'):
            self.pre_banner()
            if item.banner:
                self.display(item.banner, transition=transition)
            self.post_banner(item=item)

        try:
            for icon in item:
                self.pre_icon()
                self.display(icon, transition=transition)
                self.post_icon()
        except TypeError:
            self.pre_icon()
            self.display_icon(item, transition=transition)
            self.post_icon()

    def display_icon(self, icon, transition=None):
        pass

    def clear(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass 

class ConsoleDevice(Device):
    def clear(self):
        print("========================\n")

        if transition:
            print("Transition: %s\n" % transition)
            print(self.current.transition(icon, transition))

    def display_icon(self, icon, transition=None):
        print(icon)
        self.current = icon

Device.CHOICES["stdout"] = ConsoleDevice


