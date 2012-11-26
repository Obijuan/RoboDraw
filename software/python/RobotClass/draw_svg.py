from xml.dom import minidom
import Figures as fig
import pylab
import Robot
import time


#svgfile = "circle.svg"
#svgfile = "OSHW_logo.svg"
#svgfile = "oshwi_obi_1.svg"
#svgfile = "oshwi_obi_1_rot.svg"
svgfile = "clone_wars.svg"

document = minidom.parse(svgfile)

path = document.getElementsByTagName("path")

#for e in path:
#    print e

e = path[0]

m = e.getAttribute("d")

l = m.split()

lps = [p for p in l if p!=u'm' and p!=u'z']

#-- List of points in relative coordinates. The firs one is the initial point in absolute
#-- coordinates
lp = [ (float(p.split(',')[0]), float(p.split(',')[1])) for p in lps ]

#print lp

xc,yc = (0, 0)
alp = []

for p in lp:
    x,y = p
    xc += x
    yc += y
    alp.append((xc, yc))
    
#-- Add the first point    
#alp.append(alp[0])
    
#-- Create the robot and set the connection
r = Robot.Robot(l1 = 73.0, l2 = 97.0)
r.test()
r.connect("/dev/ttyUSB0")
time.sleep(2)
r.speed(100)
    
    
#--- Create the figure with the absolute points!
f = fig.Figure(alp)

#-- Center the figure at origin (0,0)
f.center()

#-- Flip the y axis
f.flipy()

#f = f.divide(2)

#-- Scale the figure so that it fits the robot printing area
f.scale_fity(30)

#-- Translate the figure to the robot printing origin
f.translate(r.center)  


c=(cx,cy) = r.center
r.CW=.5
r.move(c)

r.draw(f, ares=1.0)



f.plot()
pylab.axis('equal');
pylab.grid(True)
pylab.show()
