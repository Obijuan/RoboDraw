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
  pylab.plot(x,y,"ko")

def division2(p, q, res):
  """The segment determined by the points p and q is divided into
  smaller segments of length res. A list with all the points
  (including p and q) is returned """
  
  #-- Maker sure all the components of p and q are float
  px=float(p[0]); py=float(p[1]);
  qx=float(q[0]); qy=float(q[1]);
  
  #-- Calculate the distance between p and q 
  dist = math.sqrt( (px-qx)**2 + (py-qy)**2 );
  
  print "Dist: {}".format(dist);
  
  #-- Calculate the number of intermediate points
  if 0 < res < dist:
    N = int(round(dist / float(res),0))-1;
  else:
    N=0;
    
  print "Points: {}".format(N)
 
  #-- Resolution on both axes
  xres = (qx - px)/(N+1);
  yres = (qy - py)/(N+1);
  
  print "xres,yres: {},{}".format(xres,yres)
 
  #-- List of intermiate points
  li = [ (px+(i+1)*xres, py+(i+1)*yres)  for i in range(N)]
  
  #-- Return the complete list, including p and q
  return [p] + li + [q]
  
def division(l, res):
  """Divide all the sergments between points into smaller segments
  of lenth res"""
  
  lo = []
  
  for i in range(len(l)-1):
    lo = lo + division2(l[i], l[i+1], res)
    
  return lo
  

def square(center, side):
  """Generate a square. It returns a list of points
     Parameters: center: (x,y) Where the center is located
                 side:  Side length (mm)
                 res: resolution (mm)
  """               
  
  #-- The four vertex of the square
  s = [(center[0]+side/2, center[1]+side/2),
       (center[0]-side/2, center[1]+side/2),
       (center[0]-side/2, center[1]-side/2),
       (center[0]+side/2, center[1]-side/2)
      ]
      
  #-- Include the first vertex at the end to close the square    
  s = s + [s[0]]
  
  return s


  
