include <obiscad/utils.scad>


module reprap_drill(r=8, h=10, roll=0)
{

  //-- Extra distance. It does not matter the value (>0)
  extra = 5;

  //-- Cubes sizes. ccube for the teardrop. dcube for truncating the top
  csize = [r, r, h];
  dsize = [csize[X], 2*csize[Y], h+extra];

//-- The object is oriented so that the flat part points to the right
rotate([0,0,-45+roll])
  difference() {

    //-- Teardrop
    union() {
      cylinder(r=r, h=h, center=true, $fn=30);

      translate([csize[X]/2, csize[Y]/2,0])
	cube(csize, center=true);
    }

    //-- Truncate the top part
    rotate([0,0,45])
    translate([dsize[X]/2 + r , 0,0])
      cube(dsize,center=true);

  }

}

reprap_drill(r=8/2, h=20);