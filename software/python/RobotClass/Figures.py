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
        
        #print "Dist: {}".format(dist);
        
        #-- Calculate the number of intermediate points
        if 0 < res < dist:
            N = int(round(dist / float(res),0))-1;
        else:
            N=0;
            
        #print "Points: {}".format(N)
        
        #-- Resolution on both axes
        xres = (qx - px)/(N+1);
        yres = (qy - py)/(N+1);
  
        #print "xres,yres: {},{}".format(xres,yres)
        
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
    
        #--- Remove doble points
        b = [lp[i] for i in range(len(lp)-1) if lp[i]!=lp[i+1]]
        b.append(lp[len(lp)-1])  #-- Add the last point
    
        return Figure(b)

    def get_xs(self):
        """Returns a list of the x coordintes of the points"""
        return [p[0] for p in self.lp]
        
    def get_ys(self):
        """Returns a list of the y coordinates of the points"""
        return [p[1] for p in self.lp]
        
    def plot(self, points=False):
        """Plot the figure. If points is True, the figure along 
        with its points are shown"""
    
        #-- Get 2 lists, with the x and y coordinates of all the points
        #x = [p[0] for p in self.lp]
        x = self.get_xs()
        y = self.get_ys()
        
        #-- Plot as lines
        pylab.plot(x,y,"b-")
        
        if points==True:
            pylab.hold(True)
        
            #-- Superpose the points
            pylab.plot(x,y,"ko")
        
    def translate(self, tras):
        """Translate the figure"""
        self.lp = [ (p[0]+tras[0], p[1]+tras[1]) for p in self.lp ]
        return self

    def get_center(self):
        """Get the (x,y) coordintates of the center"""
        
        #-------- Get the center  
        cx = (max(self.get_xs()) + min(self.get_xs())) / 2.
        cy = (max(self.get_ys()) + min(self.get_ys())) / 2.
        
        return (cx,cy)

    def center(self):
        """Translate the figure to the center"""
        cx,cy = self.get_center()
        self.translate((-cx,-cy))
        return self

    def get_size(self):
        """Get the figure size"""
        
        w = float(max(self.get_xs()) - min(self.get_xs()))
        h = float(max(self.get_ys()) - min(self.get_ys()))
        
        return (w,h)
        
    def flipy(self):
        """Flip the figure around y axis"""
        
        self.lp = [(p[0], -p[1]) for p in self.lp]
        
        return self
        
    def flipx(self):
        """Flip the figure around x axis"""
        self.lp = [(-p[0], p[1]) for p in self.lp]
         
        return self
        
    def scale(self, sf):
        """Scale the figure by the given scale factor sf"""
        
        #-- Calculate the scaled points
        self.lp = [ (p[0] * sf, sf * p[1]) for p in self.lp ]
        return self
        
    def scale_fitx(self, x):
        """Scale the figure so that the size along x axis is equal to x"""
        
        #--- Get the figure size
        w,h = self.get_size()
        
        self.scale(x / w)
        
        return self

    def scale_fity(self, y):
        """Scale the figure so that the size along y axis is equal to y"""
        
        #--- Get the figure size
        w,h = self.get_size()
        
        self.scale(y / h )
        
        return self

    def save_st(self, filename):
        """Save the figure as Sigma technology format"""
        print "Save as: {}".format(filename)
        
        f = open(filename,"w")
        
        #-- Write the number of points
        f.write(str(len(self.lp))+'\n')
        
        #-- Write all the points
        for p in self.lp:
            f.write("{0:d} {1:d} -1000 500\n".format(int(round(p[0],0)),
                                                     int(round(p[1],0))) )  
        
        f.close()
        
    def save_c(self, filename, robot, table, comments="", ares=5):
        """Save the figure as a C-table file for inserting into
        the arduino programs.
        Parameters:
          -filename: the file name (ej. data.h)
          -Robot: The robot to use for printing. It is necessary in
                  order to calculate the inverse kinematics
          -table: The C name to give to the table
          -comments: Some C comments about the data
        The points are saved as angles (in ext. degrees)
        the first one for the arm, the second for the forearm
        """
        print "Save in C. File: {}".format(filename)
        print "For robot: "
        robot.test()
        
        #-- Transform the cartesian points into the angular space
        #-- by means of the inverse kinematics
        la=[ robot.inverse_kin(p[0],p[1],decimals=1) for p in self.lp]
        
        #-- Perform the sampling in the angular space
        la = Figure(la).divide(ares).lp
        
        #-- Convert into ext. degrees
        la = [ (int(p[0]*10), int(p[1]*10)) for p in la]
        
        for a in la:
            print "({0},{1})".format(a[0]/10., a[1]/10.)
        
        #-- Transform the sampled points into cartesian points
        #-- This is for return the user the actual figure that
        #-- the robot will draw
        lp2 = [(robot.kinematics(a[0]/10.,a[1]/10.)) for a in la]
        
        f = open(filename,"w")
        f.write(comments+"\n")
        f.write("int {}[][2]=".format(table))
        f.write("{\n")
        
        
        #-- Write the angular points
        #-- WARNING! The absolute direction of rotation depend on the
        #-- the servo. In some servos, a positive value means rotation clockwise
        #-- but in other anticlockwise
        for p in la:
            f.write("{")
            #-- For SANWA servos, the angle should be changed
            #-- For Futaba, they should not be inverted
            f.write("{},{}".format(-p[0], -p[1]))
            f.write("},\n")
        
        f.write("};\n")
        f.close()
        
        #-- Return the actual figure that will be drawn
        return Figure(lp2)
        
        
class line(Figure):
    """ Generate a line. It is given by 2 points"""
    def __init__(self, p, q):
        #print "Line!"
        
        #-- List of points
        self.lp = [p,q]
        
        
class lineh(Figure):
    """Horizontal line"""
    def __init__(self, length):
        self.lp = [(-length/2,0), (length/2,0)]
  
class linev(Figure):
    """Vertical line"""
    def __init__(self, length):
        self.lp = [(0,length/2), (0,-length/2)]
        
class box(Figure):
    """A rectangle center in the origin"""
    def __init__(self, lx, ly):
        
       self.lp = [
           (lx/2,  ly/2),
           (-lx/2, ly/2),
           (-lx/2, -ly/2),
           (lx/2,  -ly/2),
           (lx/2,  ly/2) ]
           
class vgrid(Figure):
    """A vertical grid (for testing)"""
    
    def __init__(self, x, y, NV):
        """x,y: box dimensions. NV= number of vertical lines"""
        
        ##-- List of x points
        xini = -x/2.             #-- Initial x point
        xinc = x / float(NV)     #-- Distance between vertical lines
        lx = [xini + i*xinc for i in xrange(NV)]
        ly = [(-1)**i*y/2. for i in xrange(NV)]
        
        ##-- Duplicate the x coordinates
        lx2 = []
        for px in lx:
            lx2.extend([px,px])
        lx2
        
        #-- Duplicate the y coordinates
        ly2 = [-y/2.]
        for py in ly:
            ly2.extend([py,py])
           
        self.lp = [(lx2[i],ly2[i]) for i in xrange(NV*2)]   
        
        
class fromfile(Figure):
    """A figure that is read from a file (in Sigma technologies format)"""
    def __init__(self, filename):
        f = open(filename)
        
        #-- Read the first line. It should contain the number of samples (lines)
        tam = int(f.readline())
        l = []
        
        ##-- Get the (x,y) points in the l list
        for i in xrange(tam):
            row = f.readline()
            rowl = row.split()
            l = l + [(int(rowl[0]), int(rowl[1]))]
        
        self.lp = l