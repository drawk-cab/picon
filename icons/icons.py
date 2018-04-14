#!/usr/bin/python3

import re
import logging

def _skip_comments(f):
    while True:
        r = f.readline()
        if r.strip() and not r.startswith("#"):
            break
    return r

#https://github.com/python/cpython/blob/3.6/Lib/colorsys.py
#https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def _hsv_to_rgb(h, s, v):
   if s == 0.0: return (v, v, v)
   i = int(h*6.) # XXX assume int() truncates!
   f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
   if i == 0: return (v, t, p)
   if i == 1: return (q, v, p)
   if i == 2: return (p, v, t)
   if i == 3: return (p, q, v)
   if i == 4: return (t, p, v)
   if i == 5: return (v, p, q)

def _rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = maxc-minc
    rc = (maxc-r) / s
    gc = (maxc-g) / s
    bc = (maxc-b) / s
    if r == maxc: return ((bc-gc)/6.0) % 1.0, s/maxc, v
    if g == maxc: return ((2.0+rc-bc)/6.0) % 1.0, s/maxc, v
    return ((4.0+gc-rc)/6.0) % 1.0, s/maxc, v

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

    def colour(self, dh, ds, dv):
        newdata = []
        for y in range(len(self.data)):
            newline = []
            for rgb in self.data[y]:
               h, s, v = _rgb_to_hsv(*rgb)
               newline.append(_hsv_to_rgb( (h+dh) % 1.0, max(min(s+ds,1.0),0.0), max(min(v+dv,1.0),0.0) ))
            newdata.append(newline)
        return Icon(newdata)

    def transition(self, other, name):
        frames = [self]
        for x in range(1,len(self.data)):
            if name == "wipe":
                frame_data = other.data[:x] + self.data[:x]
            elif name == "scroll":
                frame_data = self.data[x:] + other.data[:x]
            else:
                logging.warn("Unknown transition type: %s" % name)
                return []
            frames.append(Icon(frame_data))
        frames.append(other)
        return frames

    def scroll(self, other):
        frames = [self]
        for x in range(1,len(self.data)):
            frames.append(Icon(frame_data))
        frames.append(other)
        return frames

    def get_pixel(self, x, y, scale=255):
        pixel_y = len(self.data) - 1 - int(float(y) * len(self.data))
        pixel_x = int(float(x) * len(self.data[pixel_y]))
        return [int(c*scale) for c in self.data[pixel_y][pixel_x]]

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


    def get(self, l, t, sc=8, w=1, h=1, hsv=(0,0,0)):
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

