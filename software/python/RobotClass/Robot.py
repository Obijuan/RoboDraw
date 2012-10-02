import math
import pylab

class Robot:
  
  #-- Robot links
  l1 = 73
  l2 = 51

  def test(self):
    print "Scara robot: l1 = {} mm, l2 = {} mm".format(self.l1,self.l2)


  def kinematics(self, alpha, beta):
    """Direct Kinematics.
    
      Parameters:
        alpha: Angle (in degrees) of the arm
        beta: Angle (in degrees) of the forearm
        
      returns: The (x,y) coordinates of the robot end
    """
    print "Direct kinematics!"
    
    ##-- Alpha is the angle refered to the y axis
    ##-- For the calculations, it is changed to the
    ##-- x axis
    q1 = alpha + 90;
   
    ##-- Convert the angles to radians
    q1 = math.radians(q1);
    q2 = math.radians(beta);
    
    print "Robot angles: ({0},{1}) degrees ".format(alpha,beta)
    
  def draw(self,alpha,beta):
    ##pylab.ion()
    x=[5]; y=[6];
    pylab.plot(x,y,'bo',markersize=20);
    pylab.show();