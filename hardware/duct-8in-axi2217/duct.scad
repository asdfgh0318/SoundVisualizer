// Pusher duct for the APC 8x4.5MR(P) on the AXI 2217/12, one piece with the motor on the Tyto 1585 stand.
// Geometry follows docs/acoustic-speculations/duct-inlet-design-rules.pdf (derived from the
// verified extracts in the papers repo): ~1 mm tip gap, lip radius ~12 % of the throat diameter,
// wall >= 10 % of D at the propeller plane, propeller behind the lip, 10 deg diffuser,
// exit area ratio 1.1-1.3.
//
// Pusher layout: the motor sits upstream of the propeller, on the inlet side. Air enters at the
// top past the Tyto motor plate, the spider and the motor, goes through the propeller and leaves
// through the diffuser at the bottom. The spider sits above the inlet; its three arms reach past
// the lip and drop as legs down the outside of the duct, each held by one radial M3 screw into a
// heat-set insert in the outer wall, so nothing crosses the outlet and the inside stays smooth.
// Needs a pusher propeller (APC 8x4.5MRP) or the motor reversed with the propeller flipped; the
// stand reads thrust with the opposite sign to a tractor set-up.
//
// z = 0 is the exit (flat face, print the duct quarters on it).
//   openscad -D 'part="quarter"' -o duct_quarter.stl duct.scad   // print 4x, pin + glue
//   openscad -D 'part="duct"'    -o duct_full.stl    duct.scad   // whole ring (~265 mm)
//   openscad -D 'part="spider"'  -o spider.stl       duct.scad   // print arms-down, legs up

part = "assembly";   // duct | quarter | spider | assembly

// ---- propeller and gap ----
prop_d   = 203.2;    // APC 8x4.5MR(P), 8 in
tip_gap  = 1.0;      // rule 1: as small as can be built; check the real gap with a feeler gauge
throat_r = prop_d / 2 + tip_gap;

// ---- inlet ----
lip_r     = 25;      // rule 2: ~12 % of throat diameter (6 % minimum = 12 mm)
lip_out_r = 5;
wall      = 30;      // rule 3: >= 0.1 * prop_d = 20 mm at the propeller plane
throat_len = 20;     // straight section around the propeller disc; must cover the blade tips' axial extent

// ---- outlet ----
diff_angle = 10;     // rule 5
diff_len   = 45;     // exit area ratio ~1.18 at 10 deg
exit_r     = throat_r + diff_len * tan(diff_angle);
outer_r    = throat_r + wall;
outer_exit_r = exit_r + 14.5;

// ---- motor stack (MEASURE these before printing) ----
prop_to_mount   = 55;    // propeller disc to the motor's rear mounting face, mm   [MEASURE]
// AXI 2208/2212/2217 rear face: 4 x M3 in a cross, one pair 19 mm apart, the other 16 mm apart
// (AXI catalogue drawing "AXI 2208 & 2212 & 2217", modelmotors.cz actual_katalog_lr.pdf p. 6).
mount_pair_a    = 19;    // spacing of one opposite pair, mm
mount_pair_b    = 16;    // spacing of the other pair, at 90 deg to the first
mount_hole_d    = 3.2;   // M3 clearance; long M3 bolts go stand plate -> spider -> motor
hub_hole_d      = 9;     // clearance for the 3.17 mm shaft end and circlip; Ø12 left 0.4 mm to the 16 mm holes [MEASURE]

// ---- spider: hub on the motor's rear face, 3 box arms, legs down the outer wall ----
arms_n     = 3;
arm_w      = 8;       // tangential width
arm_t      = 12;      // axial thickness of hub and arms
hub_r      = 22;
leg_t      = 7;       // radial thickness of the legs
leg_bolt_z = 70;      // height of the leg screws on the outer wall (outer wall is straight from z_prop to the lip)
insert_d   = 4.0;     // M3 heat-set insert in the duct wall
insert_depth = 10;
screw_d    = 3.4;
arm_angle0 = 45;      // keeps the legs off the quarter cut planes (0/90/180/270)

// ---- quarter split ----
pin_d     = 3.2;
pin_depth = 8;

$fn = 180;

z_prop  = diff_len + throat_len / 2;
z_lip0  = diff_len + throat_len;
z_top   = z_lip0 + lip_r;
z_mount = z_prop + prop_to_mount;            // motor rear face = spider's downstream face
highlight_r = throat_r + lip_r;
leg_r0  = outer_r + 0.3;                     // leg inner face, just clear of the outer wall

function arc(c, r, a0, a1, n = 24) = [for (i = [0:n]) let(a = a0 + (a1 - a0) * i / n) [c[0] + r * cos(a), c[1] + r * sin(a)]];

profile = concat(
    [[exit_r, 0], [throat_r, diff_len], [throat_r, z_lip0]],
    arc([highlight_r, z_lip0], lip_r, 180, 90),
    arc([highlight_r, z_top - lip_out_r], lip_out_r, 90, 0),
    [[outer_r, z_prop], [outer_exit_r, 0]]
);

assert(highlight_r + lip_out_r >= outer_r - 0.01, "lip and wall do not meet; raise lip_r or lower wall");
assert(wall >= 0.1 * prop_d, "rule 3: wall thinner than 10 % of the propeller diameter");
assert(z_mount > z_top + 2, "motor mount face is inside the lip; the spider would hit the duct");
assert(mount_pair_b / 2 - mount_hole_d / 2 - hub_hole_d / 2 >= 1.5, "less than 1.5 mm between the centre hole and the motor holes");
assert(leg_bolt_z > z_prop && leg_bolt_z < z_top - lip_out_r - 6, "leg screw must land on the straight outer wall");

module at_arms() { for (i = [0:arms_n - 1]) rotate([0, 0, arm_angle0 + i * 360 / arms_n]) children(); }

module duct() {
    difference() {
        rotate_extrude() polygon(profile);
        at_arms() translate([outer_r - insert_depth, 0, leg_bolt_z]) rotate([0, 90, 0]) cylinder(d = insert_d, h = insert_depth + 1, $fn = 24);
    }
}

module quarter() {
    pin_rs = [throat_r + 0.3 * wall, throat_r + 0.7 * wall];
    pin_zs = [z_prop - 15, z_prop + 8];
    difference() {
        intersection() { duct(); translate([0, 0, -1]) cube([400, 400, 400]); }
        for (r = pin_rs, z = pin_zs) {
            translate([r, 0, z]) rotate([-90, 0, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
            translate([0, r, z]) rotate([0, 90, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
        }
    }
}

// In place: downstream face of hub and arms at z_mount.
module spider() {
    leg_len = z_mount + arm_t - (leg_bolt_z - 8);
    difference() {
        union() {
            translate([0, 0, z_mount]) cylinder(r = hub_r, h = arm_t);
            at_arms() {
                translate([0, -arm_w / 2, z_mount]) cube([leg_r0 + leg_t, arm_w, arm_t]);
                translate([leg_r0, -arm_w / 2, leg_bolt_z - 8]) cube([leg_t, arm_w, leg_len]);
            }
        }
        translate([0, 0, z_mount - 1]) cylinder(d = hub_hole_d, h = arm_t + 2);
        for (p = [[mount_pair_a / 2, 0], [-mount_pair_a / 2, 0], [0, mount_pair_b / 2], [0, -mount_pair_b / 2]])
            translate([p[0], p[1], z_mount - 1]) cylinder(d = mount_hole_d, h = arm_t + 2, $fn = 24);
        at_arms() translate([leg_r0 - 1, 0, leg_bolt_z]) rotate([0, 90, 0]) cylinder(d = screw_d, h = leg_t + 2, $fn = 24);
    }
}

module prop_disc() { color("orange", 0.5) translate([0, 0, z_prop - 1]) cylinder(d = prop_d, h = 2); }
module motor()     { color("gray") translate([0, 0, z_mount - 35]) cylinder(d = 27.7, h = 35); }   // AXI 2217 body, Ø27.7 x 35 (catalogue)
module stand()     { color("DimGray", 0.6) translate([-20, -20, z_mount + arm_t]) cube([40, 40, 4]); }          // Tyto motor plate, placeholder

if (part == "duct") duct();
else if (part == "quarter") quarter();
else if (part == "spider") translate([0, 0, z_mount + arm_t]) rotate([180, 0, 0]) spider();   // arms on the bed, legs up
else { color("SteelBlue") duct(); color("DimGray") spider(); motor(); stand(); prop_disc(); }

echo(str("throat diameter ", 2 * throat_r, " mm; outer diameter ", 2 * outer_r,
         " mm; exit diameter ", 2 * exit_r, " mm; exit area / disc area ", pow(exit_r / (prop_d / 2), 2),
         "; lip radius ", 100 * lip_r / (2 * throat_r), " % Dt; propeller ", z_top - z_prop,
         " mm below the lip edge (", 100 * (z_top - z_prop) / z_top, " % of the length); motor mount face ",
         z_mount - z_top, " mm above the lip; total length ", z_top, " mm"));
