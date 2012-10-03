import math
import pylab
import numpy as np

def Trasx(x):
  """Homogeneous matrix for translation along the x axis"""
  return np.array([
      [1, 0, 0,  x],
      [0, 1, 0,  0],
      [0, 0, 1,  0],
      [0, 0, 0,  1],
    ])

def Rotz(ang):
  """Homogeneous transformation.  Rotation around the z axis
     ang is in degrees
  """
  ca = math.cos(math.radians(ang))
  sa = math.sin(math.radians(ang))
  
  return np.array([
     [ca, -sa,  0,  0],
     [sa,  ca,  0,  0],
     [0,   0,   1,  0],
     [0,   0,   0,  1]
     ])
      

##--------------------------------------------------------------------------    
class Robot:
  
  def __init__(self):
    #-- Robot links length
    self.l1 = 73
    self.l2 = 51
    
    #-- The robot origin
    self.origin = np.array([0,0,0,1]);
    

  def test(self):
    print "Scara robot: l1 = {} mm, l2 = {} mm".format(self.l1,self.l2)


  def _kin_calculations(self, alpha, beta):
    """Internal direct kinematics calculations
       All the transformation matrices are calculated
       The origins O1 and O2 located at the end of the links 1 and 2
       are returned
       Angles (alpha and beta) are in degrees
    """
    
    ##--- Alpha is the joint 1 angle, between the y axis and the link 1
    ##-- For the calculations it is better to refer to the x axis
    alpha = alpha + 90.;
    
    #-- Transformation matrices. From the reference 0 to 1, and 1 to 2
    T1 = Rotz(alpha).dot(Trasx(self.l1))
    T2 = Rotz(beta).dot(Trasx(self.l2))
    
    ##-- Final transformation
    T = T1.dot(T2);
    
    ##-- Calculate origins of the systems 1 and 2
    O1 = T1.dot(self.origin);
    O2 = T.dot(self.origin);
    
    ##-- Return them!
    return O1,O2
    
    
  def kinematics(self, alpha, beta):
    """Direct Kinematics.
    
      Parameters:
        alpha: Angle (in degrees) of the arm
        beta: Angle (in degrees) of the forearm
        
      returns: The (x,y) coordinates of the robot end
    """
    print "Direct kinematics!"
    
    tmp, O2 = self._kin_calculations(alpha,beta)
    return O2[0], O2[1]
    
  def draw(self,alpha,beta):
    #pylab.ion()
    
     ##-- Definitions for easily accesing the vector coordinates
    X = 0;  Y = 1;  Z = 2;
    
    ##-- Get the origins of links 1 and 2
    O1,O2 = self._kin_calculations(alpha,beta)
    
    ##-- Get the x,y coordinates of all the origins, for plotting
    l1_x = [self.origin[X], O1[X], O2[X]];
    l1_y = [self.origin[Y], O1[Y], O2[Y]];
    
    
    pylab.hold(False);
    
    #-- Draw the links 1 and 2
    pylab.plot(l1_x, l1_y, "b-", linewidth=5);
    pylab.hold(True);
    
    ##-- Draw the robot origin at (0,0)
    pylab.plot([0],[0], "go", markersize=15);
    
    ##-- Draw the joint 2
    pylab.plot([O1[X]], [O1[Y]], "go", markersize=15);
    
    ##-- Draw the robot end in red
    pylab.plot([O2[X]], [O2[Y]], "ro", markersize=8);
    
    pylab.grid(True);
    
    l = self.l1 + self.l2;
    extra = 20;
    ##pylab.axis('equal') 
    pylab.ylim([-extra, l+l+extra])
    pylab.xlim([-l-extra, l+extra])
    
    pylab.xlabel('X (mm)')
    pylab.ylabel('Y (mm)')
    pylab.title('RoboDraw Kinematics')
    
    pylab.show();