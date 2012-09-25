include <obiscad/utils.scad>
use <obiscad/bcube.scad>
use <obiscad/attach.scad>


//-- Servo parameters
servo_head_lx = 56;
servo_head_ly = 20;
servo_body_lx = 42;
servo_head_ddx = 48.5;
servo_head_ddy = 9.6;
servo_head_ddiam = 3.2;

//-- The servo wrap part
forearm_servo_wrap_th = 4;
forearm_sw_ext_cr = 4;
forearm_sw_ext_cres = 5;

forearm_int_cr=1;              
forearm_int_cres=4;           

//-- The connector part
connec_th = 4;

//-- From the U-part...
fp_drills_distance = 6;

//----------------------- Build the servo wrap
extra=5;

forearm_servo_wrap_size = [servo_head_lx + 2*forearm_servo_wrap_th,
                           servo_head_ly + 2*forearm_servo_wrap_th,
                           4];

servo_base_size = [servo_body_lx, servo_head_ly, forearm_servo_wrap_size[Z]+extra];


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
  bcube(forearm_servo_wrap_size, cr=4, cres=5);

  //-- Servo base
  bcube(servo_base_size,cr = forearm_int_cr, cres = forearm_int_cres);

  //-- Drills
  for (pos  = drill_table) {
    translate(pos)
      cylinder(r=servo_head_ddiam/2, h=forearm_servo_wrap_size[Z]+extra, center=true, $fn=10);
  }
}

//----------------- Connection part ---------------

connec_size = [
    (forearm_servo_wrap_size[X] - servo_body_lx)/2,
    forearm_servo_wrap_size[Y],
    20-forearm_servo_wrap_size[Z]
  ];

module connect_part()
{
 
  conn_drill_table = [
    [0,fp_drills_distance,-connec_size[Z]/2+4],
    [0,-fp_drills_distance,-connec_size[Z]/2+4],
    [0,0,-connec_size[Z]/2+4+fp_drills_distance],
  ];

  

  difference() {
    bcube(connec_size,cr=forearm_sw_ext_cr, cres=forearm_sw_ext_cres);

    translate([-connec_th,0,0])
      bcube(connec_size + VZ(extra)-VY(2*connec_th), cr=forearm_int_cr, cres=forearm_int_cres);

    //
    for (drill=conn_drill_table) {
      translate(drill)
	rotate([0,90,0])
	  cylinder(r=servo_head_ddiam/2, h=connec_size[X]+extra, center=true, $fn=20);
    } 

  }
}


//------ Build everything

*connect_part();

a = [[forearm_servo_wrap_size[X]/2,0, forearm_servo_wrap_size[Z]/2], [0,0,1], 0];
b = [[connec_size[X]/2,0, -connec_size[Z]/2], [0,0,1], 0];

*connector(a);
*connector(b);

attach(a,b)
connect_part();





