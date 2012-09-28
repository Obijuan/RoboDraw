%%------------------------------------------------------------------
%%  Robodraw Direct kinematics
%%------------------------------------------------------------------

%%--------------------------------------------------------------------------
%%-- Draw the robot
%%-- Input: q1 and q2 are the angles (in degrees) of the arm and forearm
%%------------------------------------------------------------------------
function robot_draw(q1,q2)

%%--- q1 is the angle refered to the y axis.
%%--  for the calculations change it to the x axis
q1 = q1 + 90;

%%-- Conversion to radians
q1= q1*pi/180;
q2= q2*pi/180;

%%-- Links length (mm)
l1 = 73; 
l2 = 51;

%%-- Homogeneous transformations
A1 = Rotz(q1)*Trasx(l1);  %-- From ref. system 1 to 0
A2 = Rotz(q2)*Trasx(l2);  %-- From ref. system 2 to 1

%-- Final transformation
T = A1*A2;

%%-- Calculate the orgin coordinates of the systems 1 and 2
P01 = A1*[0 0 0 1]';
P02 = A1*A2*[0 0 0 1]';

%-- Draw the robot

x = [0 P01(1) P02(1)];
y = [0 P01(2) P02(2)];

hold off;
plot(x,y,'-o','linewidth',4);
hold on;

l = l1 + l2 + 0.5*l1;
axis([-l l -l l]);
axis('off');


