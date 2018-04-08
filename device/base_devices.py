#!/usr/bin/python3

class Device:
    CHOICES = {}

    def __init__(self):
        self.current = None

    def display(self, icon, transition=None):
        if transition is not None:
            print("Transition: %s\n" % transition)
            print(self.current.transition(icon, transition))
        print(icon)
        self.current = icon

    def clear(self):
        print("\n" * 8)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass 

Device.CHOICES["stdout"] = Device


