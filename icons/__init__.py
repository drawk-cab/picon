#!/usr/bin/python3

import re

def _skip_comments(f):
    while True:
        r = f.readline()
        if r.strip() and not r.startswith("#"):
            break
    return r

class Icon:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        s = ''
        for y in range(len(self.data)):
            for x in self.data[y]:
                s += 'R'*(x[0]>0.9) or 'r'*(x[0]>0.4) or ' '
                s += 'G'*(x[1]>0.9) or 'g'*(x[1]>0.4) or ' '
                s += 'B'*(x[2]>0.9) or 'b'*(x[2]>0.4) or ' '
            s += '\n'
        return s

    def get_pixels(self, scale=255, w=8, h=8):
        d = []
        for y in range(min(h,len(self.data))):
            l = [[int(r*scale), int(g*scale), int(b*scale)] for r,g,b in self.data[y]][:w]
            while len(l)<w:
                l.extend([0,0,0])
            d.extend(l)
        while len(d)<w*h:
            d.extend([0,0,0])
        return d
            

class IconSet:
    def __init__(self, ppm_file):
        with open(ppm_file,'r') as f:
            ppm = _skip_comments(f)
            if ppm.strip() != 'P3':
                raise NotImplementedError("icon images must be PPM-ASCII (P3)")
            self.width, self.height = (int(x) for x in filter(lambda x:x, re.split('[^A-Z0-9]+', _skip_comments(f))))
            max = int(_skip_comments(f))
            first_line = _skip_comments(f)
            self.data = [float(x)/max for x in filter(lambda x:x, re.split('[^A-Z0-9]+', first_line + f.read()))]
            if len(self.data) != self.width*self.height*3:
                raise ValueError("Data had length %s but should have been %s*%s*3 = %s" % (len(self.data), self.width, self.height, self.width*self.height*3))


    def get(self, l, t, sc=8, w=1, h=1):
        if sc:
            l *= sc
            t *= sc
            w *= sc
            h *= sc

        if l+w > self.width:
            raise ValueError("x out of range")
        if t+h > self.height:
            raise ValueError("y out of range")

        data = []
        for line in range(h):
            start = l + (t+line)*self.width
            line_data = []
            for offset in range(start, start+w):
                line_data.append(self.data[offset*3:offset*3+3])
            data.append(line_data)

        return Icon(data)

