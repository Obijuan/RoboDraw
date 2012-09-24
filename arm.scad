include <obiscad/utils.scad>
use <obiscad/bcube.scad>
use <obiscad/attach.scad>
use <obiscad/bevel.scad>


//-- Servo parameters
servo_head_lx = 56;
servo_head_ly = 20;
servo_body_lx = 42;
servo_head_ddx = 48.5;
servo_head_ddy = 9.6;
servo_head_ddiam = 3.2;

//-- The servo wrap part
arm_servo_wrap_th = 4;
arm_servo_wrap_hi = 4;
arm_sw_ext_cr = 4;
arm_sw_ext_cres = 5;

arm_int_cr=1;              
arm_int_cres=4;           

//-- Threaded rod ears
rod_dist = 28;  //-- distance between rods (between the nearer surfaces)
ear_drill = 8;
ear_nut = 14.6;
ear_extra = 1;
ear_hi = 10;
ear_cr = 4;
ear_cres = 5;


//----------------------- Build the servo wrap
extra=5;

arm_servo_wrap_size = [servo_head_lx + 2*arm_servo_wrap_th,
                       servo_head_ly + 2*arm_servo_wrap_th,
                       arm_servo_wrap_hi];

servo_base_size = [servo_body_lx, servo_head_ly, arm_servo_wrap_size[Z]+extra];


//-- Drills for the servo_wrap
//---------------------------------------
//-- DATA for the drills
//---------------------------------------
//-- Calculate the drill coordinates from the center of the base
dx=servo_head_ddx/2;
dy=servo_head_ddy/2;

//-- Build the drill table, for automating the process of 
//-- making drills
//-- All the drill are symetric respect the x and y axis
drill_table = [
  [dx,   dy, 0],
  [-dx,  dy, 0],
  [-dx, -dy, 0],
  [dx,  -dy, 0],
];


difference() {
  //-- The servo wrap base
  bcube(arm_servo_wrap_size, cr=4, cres=5);

  //-- Servo base
  bcube(servo_base_size,cr = arm_int_cr, cres = arm_int_cres);

  //-- Drills
  for (pos  = drill_table) {
    translate(pos)
      cylinder(r=servo_head_ddiam/2, h=arm_servo_wrap_size[Z]+extra, center=true, $fn=10);
  }
}

//---------------------- Build the ears
ear_ly = (rod_dist/2 - servo_base_size[Y]/2) + ear_drill + (ear_nut - ear_drill)/2 + ear_extra;
ear_lx = ear_nut + ear_extra;
ear_size = [ear_lx, ear_ly, ear_hi];

//-- Constant: minimal distance between rods...
rod_dist_min = servo_base_size[Y] + (ear_nut - ear_drill);
echo("Min: ",rod_dist_min);

module ear()
{

  ap = [
    [[-ear_size[X]/2, ear_size[Y]/2,0], [0,0,1],0],
    [[-ear_size[X]/2, ear_size[Y]/2,0],[-1,1,0],0]
  ];

   bp = [
    [[ear_size[X]/2, ear_size[Y]/2,0], [0,0,1],0],
    [[ear_size[X]/2, ear_size[Y]/2,0],[1,1,0],0]
  ];

  //connector(bp[0]);
  //connector(bp[1]);
  

  difference() {
    cube(ear_size, center=true);
    cylinder(r=ear_drill/2, h=ear_size[Z]+extra, center=true, $fn=20);
    bevel(ap[0],ap[1], l=ear_size[Z]+extra, cr=ear_cr, cres=ear_cres);
    bevel(bp[0],bp[1], l=ear_size[Z]+extra, cr=ear_cr, cres=ear_cres);
  }
}


//-- One ear
ear_conn = [[0,-ear_size[Y]/2, -ear_size[Z]/2], [0,1,0],0];

//-- Connector for upper ear (y>0)
a = [[servo_base_size[X]/2, servo_base_size[Y]/2 + arm_servo_wrap_hi ,-arm_servo_wrap_th/2 ],[0,1,0],0];

//-- Connector for lower ear (y<0)
b = [[servo_base_size[X]/2, -servo_base_size[Y]/2 - arm_servo_wrap_hi ,-arm_servo_wrap_th/2 ],[0.000001,-1,0],0];


attach(a, ear_conn)
  ear();

attach(b, ear_conn)
  ear();


p1 = [
  [[servo_base_size[X]/2, servo_base_size[Y]/2 + arm_servo_wrap_hi ,arm_servo_wrap_th/2 ], [1,0,0],0],
  [[servo_base_size[X]/2, servo_base_size[Y]/2 + arm_servo_wrap_hi ,arm_servo_wrap_th/2 ], [0,-1,1],0],
];

p2 = [
  [[servo_base_size[X]/2, -servo_base_size[Y]/2 - arm_servo_wrap_hi ,arm_servo_wrap_th/2 ], [1,0,0],0],
  [[servo_base_size[X]/2, -servo_base_size[Y]/2 - arm_servo_wrap_hi ,arm_servo_wrap_th/2 ], [0,1,1],0],
];


 %connector(p2[0]);
 %connector(p2[1]);

  bconcave_corner_attach (p1[0],p1[1],l=ear_size[X],cr=arm_servo_wrap_th,cres=0);
    bconcave_corner_attach (p2[0],p2[1],l=ear_size[X],cr=arm_servo_wrap_th,cres=0);




