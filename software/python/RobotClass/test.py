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


##-- TODO:
#-- Implement the flipx and flipy methods
#-- Implement the get_size() method
#-- Implement the scale() method

#-- Read the figure from a file
a = fig.fromfile("test.st")

#-- Center the figure at origin (0,0)
a.center()

#-- Flip the y axis
a.flipy()

#-- Scale the figure so that it fits the robot printing area
Rx = 45.
a.scale_fitx(Rx)

#-- Translate the figure to the robot printing origin
a.translate(r.center)

#-- Plot the figure
a.plot()


c = r.center
r.display_xy(c[0], c[1])
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
