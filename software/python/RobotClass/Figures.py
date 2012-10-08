import pylab
import math

  
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

class Figure():
    
    def __init__(self, lp):
        """Create a new figure from a list of points"""
        
        print "Figure: init!"
        
        #-- Just copy the list of points
        self.lp = lp
        
    def test(self):
        print "Figure!"
        
        
    def _division2(self, p, q, res):
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
        
    
    def divide(self, res):
        """Divide all the sergments between points into smaller segments
        of lenth res. It does not change the current figure, just returns
        a new one"""
        
        lp = []
        for i in range(len(self.lp)-1):
            lp.extend(self._division2(self.lp[i], self.lp[i+1], res))
    
        return Figure(lp)

    def plot(self):
        """Plot the figure"""
    
        #-- Get 2 lists, with the x and y coordinates of all the points
        x = [p[0] for p in self.lp]
        y = [p[1] for p in self.lp]
        
        #-- Plot as lines
        pylab.plot(x,y,"b-")
        
        pylab.hold(True)
        
        #-- Superpose the points
        pylab.plot(x,y,"ko")
        
    def translate(self, tras):
        """Translate the figure"""
        self.lp = [ (p[0]+tras[0], p[1]+tras[1]) for p in self.lp ]
        return self
        
        
class line(Figure):
    """ Generate a line. It is given by 2 points"""
    def __init__(self, p, q):
        print "Line!"
        
        #-- List of points
        self.lp = [p,q]
        
        
class lineh(Figure):
    """Horizontal line"""
    def __init__(self, length):
        self.lp = [(-length/2,0), (length/2,0)]
  
