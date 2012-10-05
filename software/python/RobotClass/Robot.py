import math
import pylab
import numpy as np
import serial
import time
import Figures as fig

def Plot_points(lp):
  """Plot a list of points. Each point is a pair (x,y)"""
  
  #-- Get 2 lists, with the x and y coordinates of all the points
  x = [p[0] for p in lp]
  y = [p[1] for p in lp]
  
  #-- Plot as lines
  pylab.plot(x,y,"b-")
  
  #-- Superpose the points
  pylab.plot(x,y,"ko")

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
    
    #-- Robot workspace center
    self.center = (0,90 + (self.l1+self.l2 - 90)/2 )
    
    #-- The robot origin
    self.origin = np.array([0,0,0,1]);
    
    #-- Serial port
    self.serial=object()
    
    #-- Current angular positions
    self.alpha = 0 #-- Joint 1
    self.beta = 0  #-- Joint 2
    
    #-- Set the default speed
    self.cspeed = 50
    
    #-- Constant: slowest servo angular velocity
    #-- (servo angular velocity when speed=1)
    self.CW=2.432
    

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
    tmp, O2 = self._kin_calculations(alpha,beta)
    return O2[0], O2[1]


  def inverse_kin(self, x, y, decimals=1):
    """Inverse Kinematics. It returns the angles (in degrees) """
    
    #-- x,y are float numbers (just in case)
    x=float(x)
    y=float(y)
    
    #-- Calculate the anges q1, q2, in radians
    cq2 = (x**2 + y**2 - self.l1**2 - self.l2**2)/(2*self.l1*self.l2) ;
    q2 = -math.acos(cq2);
    
    if (x==0): 
      ang = math.pi/2;
    else:
      ang = math.atan2(y,x);
    
    q1 = ang - math.atan(-self.l2*math.sqrt(1-cq2*cq2)/(self.l1+self.l2*cq2) );
    
    #-- Convert the angles to degrees
    q1 = math.degrees(q1);
    q2 = math.degrees(q2);
    
    #-- Refer the q1 angle to the y axis
    q1 = q1 - 90;
    
    #-- Truncate the angles for having the specified decimals
    q1 = round(q1, decimals)
    q2 = round(q2, decimals)
    
    #-- Return the angles
    return q1,q2

  def connect(self, serial_str):
    """Open the serial port"""
    self.serial = serial.Serial(serial_str, 9600) 

  def speed(self,speed):
    """Set the robot speed (0 - 127)"""
    self.serial.write("V"+str(speed)+" ");
    self.cspeed = speed

  def pose_get(self):
    """Return the current angular pose"""
    return (self.alpha, self.beta)
    
  def time_to_reach(self, alpha, beta):
    """Estimate the time it takes to the servos to reach
       the target alpha,beta angles from the current position 
       The alpha and beta are in degrees
    """

    dist = float( max(abs(alpha-self.alpha), abs(beta-self.beta)) )
    stime = dist / (self.CW * self.cspeed)
    print "Dist: {}".format(dist)
    
    #-- Return the estimated time
    return stime
    
  def pose(self, alpha, beta, wait=True):
    """Set the angles of the joints of RoboDraw (in degrees)"""
    
    #-- Convert into extended degrees
    # Extended degrees are float degrees with only one decimal, multiply
    # by 10. So that only integer numbers are used
    # Example:  852 extende degrees (integer) means 85.2 degrees (float)
    alpha_ext = int(round(alpha*10 ,0));
    beta_ext =  int(round(beta*10, 0));
    print "Pose: ({},{}) Ext. degrees".format(alpha_ext, beta_ext)
    
    self.serial.write("P"+str(alpha_ext)+","+str(beta_ext)+" ")
    
    if wait:
      #-- Wait until the new pos is reached
      time.sleep( self.time_to_reach(alpha,beta) )
    
    #-- Write the current angular pos
    self.alpha = alpha;
    self.beta = beta;
    
  def move(self, p):
    """Move RoboDraw to the point p (x,y) (in mm)"""
    
    ##-- Transform the (x,y) point into the angular space
    q1,q2 = self.inverse_kin(p[0],p[1],decimals=1)
    self.pose(q1,q2);
    
  def draw(self, l,res):
    """Make the RoboDraw Draw the figure determined by the listo of points"""

    #-- First, the segments are "sampled", generating more points
    #-- separated by res mm
    ls = fig.division(l, res)
    
    #-- Move to all the points in the list :-)
    for p in ls:
      self.move(p)
    
  def display_draw(self, l, res, decimals=1):
    """Draw the figure given by the list of points l. It is drawn
    by means of the virtual robot (applying inverse kinematics to
    the points, and then the direct kinematics"""
    
    #-- First, the segments are "sampled", generating more points
    #-- separated by res mm
    ls = fig.division(l, res)
    
    #-- Transform the cartesian points into the angular space
    #-- by means of the inverse kinematics
    la=[ ( self.inverse_kin(p[0],p[1],decimals) ) for p in ls]
    
    #-- Transform the angular space into cartesian again, by means
    #-- of the direct kinematics
    lc = [ (self.kinematics(a[0],a[1])) for a in la]
    
    #-- Draw the object
    Plot_points(lc);
    

  def display_xy(self, x, y, decimals=1):
    """Draw the robot from the (x,y) coordinates of the end"""
    
    ##-- Calculate the angles
    q1,q2 = self.inverse_kin(x,y,decimals)
    
    #-- Draw the robot
    self.display(q1,q2);
    
    
  def display(self,alpha,beta):
    """Draw the robot, from the 2 angles
    """
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