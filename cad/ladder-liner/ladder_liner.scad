// Ladder liner for a circular slot. Two ways to print it:
//   mode = "ring"    : printed standing up, already curled to the slot (axis = Z, ring is H tall,
//                      wall = `wall` thick), with a dovetail latch closing the seam.
//   mode = "segment" : one flat, 0.6 mm (layers x layer) segment, to be rolled afterwards.
//   mode = "full"    : the flat segments side by side, for reference.
// Axes in the flat strip: X along the strip (circumference), Y across it (slot height), Z thickness.
D_in      = 210;    // slot inner diameter, mm
H         = 100;    // slot height = strip width, mm
layer     = 0.2;    // layer height, flat mode
layers    = 3;      // flat mode: 2-3 layers
wall      = 0.8;    // ring mode: radial wall thickness (two 0.4 mm perimeters)
rail      = 4;      // rail width along the top and bottom edges
rung_w    = 4;      // strut width
n_struts  = 10;     // vertical struts per segment (excluding the two end blocks)
segments  = 1;      // 1 = whole ring in one piece, one latch
block     = 9;      // wide end block that carries the dovetail
tab_len   = 5;      // dovetail length
neck      = 6;      // dovetail neck width
head      = 10;     // dovetail head width
clr       = 0.25;   // latch clearance per side

mode = "ring";      // "ring" | "segment" | "full"

t   = (mode == "ring") ? wall : layer*layers;
Rm  = (D_in - t)/2;           // mid-wall radius
Ri  = D_in/2 - t;             // inner radius
L   = 2*PI*Rm;                // strip length along the mid-wall
E   = L/segments;
gap = (E - 2*block - n_struts*rung_w)/(n_struts + 1);
strut_x = [for (i = [1:n_struts]) block + gap*i + rung_w*(i-1)];

module dovetail(c=0) polygon([[-0.01, -(neck/2+c)], [tab_len*0.4, -(neck/2+c)],
    [tab_len+c, -(head/2+c)], [tab_len+c, head/2+c],
    [tab_len*0.4, neck/2+c], [-0.01, neck/2+c]]);

// ---- flat segment -------------------------------------------------
module flat_body() difference() {
  union() {
    cube([E, rail, t]);
    translate([0, H-rail, 0]) cube([E, rail, t]);
    cube([block, H, t]);
    translate([E-block, 0, 0]) cube([block, H, t]);
    for (x = strut_x) translate([x, 0, 0]) cube([rung_w, H, t]);
  }
  translate([0, H/2, -1]) linear_extrude(t+2) dovetail(clr);
}
module flat_segment() union() {
  flat_body();
  translate([E, H/2, 0]) linear_extrude(t) dovetail(0);
}

// ---- standing ring ------------------------------------------------
module sector(x0, x1, z0, z1)
  rotate([0, 0, 360*x0/L]) translate([0, 0, z0])
    rotate_extrude(angle = 360*(x1-x0)/L, $fn = 720)
      translate([Ri, 0]) square([t, z1-z0]);

module latch(c, pad=0) translate([Ri-pad, 0, 0]) rotate([90,0,90])
  linear_extrude(t+2*pad) translate([0, H/2]) dovetail(c);

module ring() {
  difference() {
    union() {
      sector(0, E, 0, rail);
      sector(0, E, H-rail, H);
      sector(0, block, 0, H);
      sector(E-block, E, 0, H);
      for (x = strut_x) sector(x, x+rung_w, 0, H);
    }
    latch(clr, 1);                                // pocket in the start block
  }
  latch(0);                                      // tab on the end block, engaging the pocket
}

if (mode == "ring") ring();
else if (mode == "segment") flat_segment();
else for (i = [0:segments-1]) translate([i*E, 0, 0]) flat_segment();
echo(mode=mode, L=L, E=E, gap=gap, t=t, Ri=Ri);
