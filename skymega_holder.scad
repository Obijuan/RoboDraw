include <obiscad/utils.scad>
use <obiscad/bcube.scad>
use <obiscad/attach.scad>


//------------------------ Data for the Rod holders
rod_hold_len = 15;

//--- Distance from the base to the rod (not the center)
rod_hold_drill_hi = 11;
rod_hold_drill_diam = 8.3;
rod_hold_th = 2;

//-- Data for the skymega

skymega_size = [52, 52, 3];
skymega_cr = 3;
skymega_cres = 5;
skymega_drill_diam=3.2;

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
      cylinder(r=rod_hold_drill_diam/2, h=rod_holder_size[X]+extra, center=true, $fn=20);
  }

}


//-- Build the base

difference() {
  bcube(skymega_size, cr=skymega_cr, cres=skymega_cres);

  for (drill = drill_table) {
    translate(drill)
      cylinder(r=skymega_drill_diam/2, h=skymega_size[Z]+extra,center=true, $fn=20); 
  }
}

a = [[0, -skymega_size[Y]/2, skymega_size[Z]/2],[0,0,1],0];
b = [[0, skymega_size[Y]/2, skymega_size[Z]/2],[0,0,1],180];

c = [[0, -rod_holder_size[Y]/2, -rod_holder_size[Z]/2],[0,0,1],0];

*connector(a);
*connector(b);
*connector(c);

attach(a,c)
  rod_holder();

attach(b,c)
  rod_holder();



