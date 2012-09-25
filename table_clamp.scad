include <obiscad/utils.scad>
use <obiscad/bcube.scad>
use <obiscad/attach.scad>
use <obiscad/bevel.scad>

servo_wrap_th = 4;

//-- Clamp
//-- BUG: there is a bug in the arm calculation of the rod distance. For that
//-- reason the term servo_wrap_th*2 has to be added
rod_dist = 28+2*servo_wrap_th;  //-- distance between rods (between the nearer surfaces)
clamp_drill = 8;
clamp_nut = 14.6;
clamp_extra = 1;
clamp_hi = 10;
clamp_cr = 4;
clamp_cres = 5;
clamp_th = 5;
clamp_lx = 30;


//---------- DATA ----------------
extra=5;

tower_lx = clamp_nut + 2*clamp_extra;
tower_ly = rod_dist + 2*(clamp_drill) + (clamp_nut - clamp_drill) + 2*(clamp_extra);
clamp_body_size = [ tower_lx + clamp_lx, tower_ly, clamp_hi ];

drills_x = clamp_body_size[X]/2 - tower_lx/2;
drills_y = rod_dist/2 + clamp_drill/2;
pos1 = [drills_x, drills_y,  0];
pos2 = [drills_x, -drills_y, 0];

echo("pos1: ",pos1);



difference() {
  bcube(clamp_body_size, cr=clamp_cr, cres=clamp_cres);

  translate(pos2)
    cylinder(r=clamp_drill/2, h=clamp_body_size[Z]+extra, center=true, $fn=20);


  translate(pos1)
    cylinder(r=clamp_drill/2, h=clamp_body_size[Z]+extra, center=true, $fn=20);

  //-- Remove the upper part to create the base that will be in contact 
  //-- with the table
  translate([-tower_lx,0,clamp_hi - clamp_th])
    cube(clamp_body_size+VY(extra),center=true);
}


