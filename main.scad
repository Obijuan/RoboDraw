include <obiscad/utils.scad>
use <lib.scad>


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


//------------------ Front plate

extra = 5;

//-- Front plate size
front_plate_size = [u_lx + 2*thickness, u_ly, thickness];


*difference() {

  //-- Draw the front plate base
  cube(front_plate_size, center=true);

  //-- Drills. There are 4 drills on a circle of fp_drills_distance radius
  for (i=[0:3]) {
    rotate([0,0,i*90])
      translate([fp_drills_distance,0,0])
        cylinder(r=fp_drills_diam/2, h=thickness+extra, center=true, $fn=10);
  }
}

//------------------- Fake shaft ear ------------------

fs_body_size = [u_shaft_front_dist, u_ly, thickness];



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



