#!/usr/bin/python
# -*- coding: utf-8 -*-

import Robot
import pylab
#import math
import time
import Figures as fig
import numpy as np

def test_figure(filename, lenx, robot):
    """Read a figure from a file and apply transformation so that
    it can be printed on the robot
    Parameters:
      -filename: The file in ST format
      -lenx: Scale the figure so that the width is equal to lenx
      -robot: The robot"""
      
    #-- Read the figure from a file
    f = fig.fromfile(filename)
    
    #-- Center the figure at origin (0,0)
    f.center()

    #-- Flip the y axis
    f.flipy()

    #-- Scale the figure so that it fits the robot printing area
    f.scale_fitx(lenx)

    #-- Translate the figure to the robot printing origin
    f.translate(robot.center)  
      
    return f

    
#------- Main     
    
r = Robot.Robot()
r.test()
r.connect("/dev/ttyUSB0")
time.sleep(2)

pylab.ion()

#-- Read the figure from a file
a = test_figure("test.st", 40, r)

#-- Plot the figure
a.plot()


c = r.center
r.display_xy(c[0], c[1])
r.move(c)
#r.draw(a)



#-- Plot the center
#pylab.plot([0], [0], "ro", markersize=10)
#pylab.grid(True)
#pylab.axis("equal")



#l2 = [ (c[0],c[1]+15), (c[0],c[1]-15)]
#l = [(c[0]-50,c[1]), (c[0]+50,c[1])]
#s = fig.square(r.center, 30)
#r.move(c);
#r.display_draw(s,5)
