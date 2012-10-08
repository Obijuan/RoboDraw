#!/usr/bin/python
# -*- coding: utf-8 -*-

import Robot
import pylab
#import math
import time
import Figures as fig
import numpy as np

r = Robot.Robot()
r.test()
r.connect("/dev/ttyUSB0")
time.sleep(2)

pylab.ion()


#-- Read the figure from a file
a = fig.fromfile("sign027.st")

#-- Center the figure at origin (0,0)
a.center()

lx = np.array(a.get_xs()) #np.array(lx) - cx
ly = np.array(a.get_ys()) #np.array(ly) - cy

#-- Flip the y axis
ly = -ly

#-- Get the height and width of the sign
w = float(max(lx) - min(lx))
h = float(max(ly) - min(ly))

#-- Robot printing area (where the sign will be printed)
Rx = 45.
Ry = (h / w) * Rx

#-- Scale the sign to fit on the robot printing area. Traslate it
#-- to the robot origin
lx = lx * Rx / w + r.center[0]
ly = ly * Ry / h + r.center[1]


pylab.plot(lx, ly, "b-")
#pylab.plot(lx, ly, "ko")

c = r.center
r.display_xy(lx[0], ly[0])


#-- Build the new list of points
l = [(lx[i], ly[i]) for i in range(len(lx))]

f = fig.Figure(l)

r.move(c)



#-- Plot the center
#pylab.plot([0], [0], "ro", markersize=10)
#pylab.grid(True)
#pylab.axis("equal")



#l2 = [ (c[0],c[1]+15), (c[0],c[1]-15)]
#l = [(c[0]-50,c[1]), (c[0]+50,c[1])]
#s = fig.square(r.center, 30)
#r.move(c);
#r.display_draw(s,5)
