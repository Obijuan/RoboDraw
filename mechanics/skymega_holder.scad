include <obiscad/utils.scad>
use <obiscad/bcube.scad>
use <obiscad/attach.scad>
use <lib.scad>


//------------------------ Data for the Rod holders
rod_hold_len = 15;

//--- Distance from the base to the rod (not the center)
rod_hold_drill_hi = 11;
rod_hold_drill_diam = 8.3;
rod_hold_th = 2;

servo_wrap_th = 4;

//-- Clamp
//-- BUG: there is a bug in the arm calculation of the rod distance. For that
//-- reason the term servo_wrap_th*2 has to be added
rod_dist = 28+2*servo_wrap_th;  //-- distance between rods (between the nearer surfaces)

//-- Data for the skymega

base_size = [52, rod_dist+2*rod_hold_drill_diam+2*rod_hold_th, 3];
base_cr = 3;
base_cres = 5;
base_drill_diam=3.2;

//-- Skymega drills
dd = 15;

drill_table = [
  [dd,   dd, 0],
  [-dd,  dd, 0],
  [-dd, -dd, 0],
  [dd,  -dd,  0],
];

extra=5;

//-- Rod holders

rod_holder_size = [rod_hold_len, 
                   rod_hold_drill_diam + 2*rod_hold_th, 
                   rod_hold_drill_hi+rod_hold_drill_diam/2];

module rod_holder()
{

 
  difference() {
    union() {
      //-- Rod holder main body
      cube(rod_holder_size,center=true);

      translate([0,0,rod_holder_size[Z]/2])
	rotate([0,90,0])
	  cylinder(r=rod_hold_drill_diam/2+rod_hold_th, h=rod_holder_size[X], center=true, $fn=20);
    }

   //-- Big drill
   translate([0,0,rod_holder_size[Z]/2])
    rotate([0,90,0])
      //cylinder(r=rod_hold_drill_diam/2, h=rod_holder_size[X]+extra, center=true, $fn=20);
      reprap_drill(r=rod_hold_drill_diam/2, h=rod_holder_size[X]+extra, roll=180);
  }

}


//-- Build the base

difference() {
  bcube(base_size, cr=base_cr, cres=base_cres);

  for (drill = drill_table) {
    translate(drill)
      cylinder(r=base_drill_diam/2, h=base_size[Z]+extra,center=true, $fn=20); 
  }
}

a = [[0, -base_size[Y]/2, base_size[Z]/2],[0,0,1],0];
b = [[0, base_size[Y]/2, base_size[Z]/2],[0,0,1],180];

c = [[0, -rod_holder_size[Y]/2, -rod_holder_size[Z]/2],[0,0,1],0];

*connector(a);
*connector(b);
*connector(c);

attach(a,c)
  rod_holder();

attach(b,c)
  rod_holder();



