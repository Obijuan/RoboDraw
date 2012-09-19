include <obiscad/utils.scad>
use <lib.scad>
use <obiscad/attach.scad>


//-- U part

thickness = 4;

//-- Distance from the servo shaft to the front plate
u_shaft_front_dist = 20;

//-- Distance from the servo shaft to the rear  
u_shaft_rear_dist = 13;

u_lx = 40;
u_ly = 25;
u_lz = u_shaft_front_dist + u_shaft_rear_dist;

//-- Front plate user params
//-- Distance between the center and the drills (radius)
fp_drills_distance = 8;

//-- Drills diameter
fp_drills_diam = 3.2;

//-- Fake shaft ear params
fs_diam = 8;  //-- Fake shaft diam

//-- Shaft ear params
s_diam = 8.1;            //-- Servo horn Shaft diameter
horn_drill_diam = 2;   //-- horn drills diameter

//-- Radial distance of the rounded servo horn drills
rounded_horn_drill_distance = 7.3;

//------------------------------------------------------------------------
extra = 5;


//------------------- Fake shaft ear ------------------
module fs_ear()
{
  fs_body_size = [u_shaft_front_dist, u_ly, thickness];

  //--- Build the part!


  difference() {

    //-- Main fake shaft ear body
    union() {
      cylinder(r=u_ly/2, h=thickness, center=true);

      translate([fs_body_size[X]/2,0,0])
	cube(fs_body_size, center=true);
    }

    //-- Fake shaft drill
    *cylinder(r=fs_diam/2, h=thickness+extra, center=true);
    reprap_drill(r=fs_diam/2, h=thickness+extra, roll=180);
  }

}


//------------------- Shaft ear ---------------------------
module s_ear()
{
  s_body_size = [u_shaft_front_dist, u_ly, thickness];

  s_cutout_size = [u_ly/2+extra, s_diam, s_body_size[Z]+extra];


  difference() {

    //-- Main fake shaft ear body
    union() {
      cylinder(r=u_ly/2, h=thickness, center=true);

      translate([s_body_size[X]/2,0,0])
	cube(s_body_size, center=true);
    }

    //-- Fake shaft drill
    cylinder(r=s_diam/2, h=thickness+extra, center=true);
    
    //-- Cutout
    translate([-s_cutout_size[X]/2,0,0])
      cube(s_cutout_size,center=true);

    //-- Rounded servo horn drills
    for (i=[0:2]) {
      rotate([0,0,-90*i])
        translate([0, rounded_horn_drill_distance, 0])
          cylinder(r=horn_drill_diam/2, h=s_body_size[Z]+extra, center=true, $fn=10);
    }

  }

}


//------------------ Front plate
//-- Front plate size
front_plate_size = [u_lx + 2*thickness, u_ly, thickness];



difference() {

  //-- Draw the front plate base
  cube(front_plate_size, center=true);

  //-- Drills. There are 4 drills on a circle of fp_drills_distance radius
  for (i=[0:3]) {
    rotate([0,0,i*90])
      translate([fp_drills_distance,0,0])
        cylinder(r=fp_drills_diam/2, h=thickness+extra, center=true, $fn=10);
  }
}

//-- Define the connectors
s_ear_con  = [[u_shaft_front_dist,0,0], [-1,0,0], 0];
fs_ear_con = [[u_shaft_front_dist,0,0], [-1,0,0], 0];

front_plate_con1 = [[-front_plate_size[X]/2 + thickness/2, 0, front_plate_size[Z]/2], [0,0,1], 0];

front_plate_con2 = [[front_plate_size[X]/2 - thickness/2, 0, front_plate_size[Z]/2], [0,0,1], 0];


attach(front_plate_con1, s_ear_con) 
  s_ear();

attach(front_plate_con2, fs_ear_con)
  fs_ear();








