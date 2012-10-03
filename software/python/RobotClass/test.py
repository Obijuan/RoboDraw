import Robot
import pylab
import math

def Plot_points(lp):
  """Plot a list of points. Each point is a pair (x,y)"""
  
  #-- Get 2 lists, with the x and y coordinates of all the points
  x = [p[0] for p in lp]
  y = [p[1] for p in lp]
  
  #-- Plot as lines
  pylab.plot(x,y,"b-")
  
  #-- Superpose the points
  pylab.plot(x,y,"go")

def division2(p, q, res):
  
  #-- Maker sure all the components of p and q are float
  px=float(p[0]); py=float(p[1]);
  qx=float(q[0]); qy=float(q[1]);
  
  #-- Calculate the distance between p and q 
  dist = math.sqrt( (px-qx)**2 + (py-qy)**2 );
  
  print "Dist: {}".format(dist);
  
  #-- Calculate the number of intermediate points
  if res>0 and res<dist:
    N = math.trunc(dist / float(res))-1;
  else:
    N=0;
    
  print "Points: {}".format(N)
 
  
  #-- Resolution on both axes
  xres = (q[0] - p[0])/(N+1);
  yres = (q[1] - p[1])/(N+1);
  
  print "xres,yres: {},{}".format(xres,yres)
 
  #-- List of intermiate points
  li = [ (p[0]+(i+1)*xres, p[1]+(i+1)*yres)  for i in range(N)]
  
  #-- Return the complete list, including p and q
  return [p] + li + [q]
  
  
#---------------------------------------------------  
  
pylab.ion();

myrobot = Robot.Robot();

myrobot.test();
myrobot.kinematics(0,0);

myrobot.display(40,-80);

l=division2((-50,100), (50,100), 10)
Plot_points(l)