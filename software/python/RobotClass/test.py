#!/usr/bin/python
# -*- coding: utf-8 -*-


#-- TODO:
#-- New figures: polygon (and circle)
#-- Generate some data to draw autonomously: adjust the waiting time...
#-- It should draw more o less ok autonomously

import Robot
import pylab
#import math
import time
import Figures as fig
import numpy as np

def test_figure(filename, leny, robot):
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
    
    #-- Set the space resolution
    #f = f.divide(5)

    #-- Flip the y axis
    f.flipy()

    #-- Scale the figure so that it fits the robot printing area
    f.scale_fity(leny)

    #-- Translate the figure to the robot printing origin
    f.translate(robot.center)  
      
    return f

def test_save_st(filename):
    """Save a figure to the st format. Read it and display to
    test if the save_st method works"""
    
    #-- Create a box
    a = fig.box(40,20).translate(r.center)
    
    #-- Subdivide into smaller points
    a = a.divide(5)
    a.plot()
    
    #--- Save the figure as a file
    a.save_st(filename)
    
    #-- Read the file
    b = fig.fromfile(filename)
    b.plot(True)
    
def test_save_c(filename, r, tablename="data",comments="//-- Figure (ext. degrees)"):
    """Save the figure as a c-table for including into the 
    arduino files"""
    
    #-- Create a box
    a = fig.box(40,20).translate(r.center)
    
    #-- Subdivide into smaller points
    #a = a.divide(5)
    #a.plot(True)
    
    #--- Save the figure as a file
    a.save_c(filename,r,"data","//-- a Box. Resolution 5", ares=0.01)

def recursive_cube(r):
    rc = []
    for l in range(40,2,-1):
        a=fig.box(l,l).divide(2).translate(r.center)
        r.draw(a, ares=1.0)
        a.plot()
        
        #rc.extend(a.lp)
    #test = fig.Figure(rc) 
    #test = test.divide(2)
    #test.plot()
    #test.save_c("rcube.h",r,"data","//-- Recursive cube")
    return 
    

def cube_test(r):
    """Draw a test cube"""
    a=fig.box(40,25).divide(5.0).translate(r.center)
    r.display_draw(a, ares=5.0, display_points=True)
    r.draw(a,ares=5.0)

def vgrid_test(r):
    a = fig.vgrid(60,20,10).divide(2.0).translate(r.center)
    r.display_draw(a, ares=5.0, display_points=True)
    r.draw(a,ares=5.0)
    
def test_pol():
    pol = [(32.324879,901.84946),
           (210.111729,106.06604),
           (-110.106629,51.5178),
           (17.17259,125.2589),
           (-142.43151,4.0406),
           (-22.22335,-227.28434)]
           
    poly = fig.Figure(pol)
    poly.plot();
    
#------- Main     
    
r = Robot.Robot(l1 = 73.0, l2 = 97.0)
r.test()
r.connect("/dev/ttyUSB0")
time.sleep(2)
r.speed(100)

pylab.ion()


c=(cx,cy) = r.center
r.CW=2.0
r.move(c)

recursive_cube(r)
#test_pol()

#a = fig.vgrid(60,30,10).divide(2).translate(r.center)
#a = fig.box(60,30).divide(2).translate(r.center)
#c=(cx,cy) = r.center
#r.CW=0.1
#r.move(c)
#r.draw(a, ares=1.0)
#fd = a.save_c("vgrid_ares1.h",r,"data","//-- vgrid ares=1.0", ares = 1.0)
#fd.plot(True)


#f = test_figure(filename+".txt", leny=30, robot=r);
#fd = f.save_c(filename+".h",r,"data","//-- Sign", ares=3.0);
#f.plot();
#f.plot();
#pylab.axis('equal');
#pylab.grid(True)

#r.draw(f, ares=5.0)

#f.plot(True);

#test_save_st("test.st")
#test_save_c("cube.h",r)
#recursive_cube(r)


#-- Read the figure from a file
#a = test_figure("sign027.st", 40, r)

#-- Plot the figure
#a.plot(True);

#a.save_c("sign027.h",r,"data","//-- Sign");

#-- Vertical line, translated to the robot center
#a = fig.linev(30).translate(r.center)
#a.plot(True)

#c=(cx,cy) = r.center
#r.display_xy(cx, cy)
#r.move(c)
#cube_test(r)
#vgrid_test(r)


#-- Plot the center
#pylab.plot([0], [0], "ro", markersize=10)
#pylab.grid(True)
#pylab.axis("equal")



#l2 = [ (c[0],c[1]+15), (c[0],c[1]-15)]
#l = [(c[0]-50,c[1]), (c[0]+50,c[1])]
#s = fig.square(r.center, 30)
#r.move(c);
#r.display_draw(s,5)
