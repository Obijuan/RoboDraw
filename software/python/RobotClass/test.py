import Robot
import pylab
import math
import time
import Figures as fig


r = Robot.Robot();
r.test();
r.connect("/dev/ttyUSB0")
time.sleep(2);

pylab.ion();

c = r.center

r.display_xy(c[0], c[1]);

l2 = [ (c[0],c[1]+15), (c[0],c[1]-15)]

l = [(c[0]-50,c[1]), (c[0]+50,c[1])]

s = fig.square(r.center, 20)

r.move(c);

r.display_draw(s,10)



