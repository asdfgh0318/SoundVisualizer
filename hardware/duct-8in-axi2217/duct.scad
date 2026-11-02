// Duct for the APC 8x4.5MR on the AXI 2217/12, one piece with the motor on the Tyto 1585 stand.
// Geometry follows docs/acoustic-speculations/duct-inlet-design-rules.pdf (derived from the
// verified extracts in the papers repo): ~1 mm tip gap, lip radius ~12 % of the throat diameter,
// wall >= 10 % of D at the propeller plane, propeller behind the lip, 10 deg diffuser, exit area
// ratio 1.1-1.3, supports >= ~11 mm behind the disc.
//
// Orientation: z = 0 is the exit (flat face, print it on the bed), the inlet lip is at the top.
// Air enters at the top and leaves at the bottom, so the motor and stand sit downstream of the
// propeller (tractor propeller pulling away from the stand).
//
// Export one part at a time:
//   openscad -D 'part="duct"'    -o duct_full.stl    duct.scad   // whole ring (~265 mm, too big for most beds)
//   openscad -D 'part="quarter"' -o duct_quarter.stl duct.scad   // print 4x, pin + glue
//   openscad -D 'part="spider"'  -o spider.stl       duct.scad   // motor plate + 3 arms
//   openscad -D 'part="section"' -o section.png      duct.scad   // half-section for checking

part = "assembly";   // duct | quarter | spider | section | assembly

// ---- propeller and gap ----
prop_d   = 203.2;    // APC 8x4.5MR, 8 in
tip_gap  = 1.0;      // rule 1: as small as can be built; check the real gap with a feeler gauge
throat_r = prop_d / 2 + tip_gap;

// ---- inlet ----
lip_r     = 25;      // rule 2: ~12 % of throat diameter (6 % minimum = 12 mm)
lip_out_r = 5;       // small rounding where the lip meets the outer wall
wall      = 30;      // rule 3: >= 0.1 * prop_d = 20 mm at the propeller plane
throat_len = 20;     // straight section around the propeller disc; must cover the blade tips' axial extent

// ---- motor stack (MEASURE these before printing) ----
prop_to_mount = 55;  // propeller disc to the motor's rear mounting face, mm  [MEASURE]
mount_holes_n   = 4;     // [MEASURE] AXI 2217 rear mount
mount_holes_pcd = 25;    // [MEASURE] hole circle diameter
mount_hole_d    = 3.2;   // M3 clearance
hub_hole_d      = 12;    // [MEASURE] clearance for the shaft end / circlip / bearing boss

// ---- outlet ----
diff_angle = 10;                              // rule 5
diff_len   = prop_to_mount - throat_len / 2;  // diffuser ends at the motor mount plane
exit_r     = throat_r + diff_len * tan(diff_angle);
outer_r    = throat_r + wall;
outer_exit_r = exit_r + 14.5;                 // flat trailing face, room for the spider tabs

// ---- spider (supports): at the exit plane, rule 6 ----
arms_n     = 3;       // odd, so the two blades never pass two arms at once
arm_w      = 6;       // tangential width
arm_depth  = 12;      // axial depth (along the flow)
hub_r      = 22;
hub_t      = 5;
tab_r      = (exit_r + outer_exit_r) / 2;     // radius of the tab bolts into the trailing face
insert_d   = 4.0;     // M3 heat-set insert hole
insert_depth = 10;
arm_angle0 = 30;      // keeps the tab holes off the quarter-segment cut planes

// ---- quarter split ----
pin_d     = 3.2;      // 3 mm pins (or 3 mm filament offcuts) + glue
pin_depth = 8;

$fn = 180;

z_throat0 = diff_len;
z_prop    = diff_len + throat_len / 2;
z_lip0    = diff_len + throat_len;
z_top     = z_lip0 + lip_r;
highlight_r = throat_r + lip_r;

function arc(c, r, a0, a1, n = 24) = [for (i = [0:n]) let(a = a0 + (a1 - a0) * i / n) [c[0] + r * cos(a), c[1] + r * sin(a)]];

profile = concat(
    [[exit_r, 0], [throat_r, z_throat0], [throat_r, z_lip0]],
    arc([highlight_r, z_lip0], lip_r, 180, 90),                            // inner lip, throat -> highlight
    arc([highlight_r, z_top - lip_out_r], lip_out_r, 90, 0),               // outer rounding
    [[highlight_r + lip_out_r, z_prop], [outer_exit_r, 0]]
);

assert(highlight_r + lip_out_r >= outer_r - 0.01, "lip and wall do not meet; raise lip_r or lower wall");
assert(wall >= 0.1 * prop_d, "rule 3: wall thinner than 10 % of the propeller diameter");
assert(prop_to_mount - throat_len / 2 >= 0.055 * 2 * throat_r, "rule 6: supports closer than ~5.5 % Dt behind the disc");

module duct() {
    difference() {
        rotate_extrude() polygon(profile);
        for (i = [0:arms_n - 1]) rotate([0, 0, arm_angle0 + i * 360 / arms_n])
            translate([tab_r, 0, -0.01]) cylinder(d = insert_d, h = insert_depth, $fn = 24);
    }
}

module quarter() {
    pin_rs = [throat_r + 0.3 * wall, throat_r + 0.7 * wall];
    pin_zs = [z_prop - 15, z_prop + 8];
    difference() {
        intersection() {
            duct();
            translate([0, 0, -1]) cube([400, 400, 400]);
        }
        for (r = pin_rs, z = pin_zs) {
            translate([r, 0, z]) rotate([-90, 0, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
            translate([0, r, z]) rotate([0, 90, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
        }
    }
}

module spider() {
    difference() {
        union() {
            translate([0, 0, -hub_t]) cylinder(r = hub_r, h = hub_t);
            for (i = [0:arms_n - 1]) rotate([0, 0, arm_angle0 + i * 360 / arms_n]) {
                hull() {                                                   // streamlined arm: round nose and tail
                    translate([hub_r - 4, 0, -arm_depth + arm_w / 2]) rotate([0, 90, 0]) cylinder(d = arm_w, h = tab_r - hub_r + 4, $fn = 24);
                    translate([hub_r - 4, 0, -arm_w / 2]) rotate([0, 90, 0]) cylinder(d = arm_w, h = tab_r - hub_r + 4, $fn = 24);
                }
                translate([tab_r, 0, -hub_t]) cylinder(d = 14, h = hub_t, $fn = 48);
            }
        }
        translate([0, 0, -50]) cylinder(d = hub_hole_d, h = 100);
        for (i = [0:mount_holes_n - 1]) rotate([0, 0, 45 + i * 360 / mount_holes_n])
            translate([mount_holes_pcd / 2, 0, -50]) cylinder(d = mount_hole_d, h = 100, $fn = 24);
        for (i = [0:arms_n - 1]) rotate([0, 0, arm_angle0 + i * 360 / arms_n])
            translate([tab_r, 0, -50]) cylinder(d = 3.4, h = 100, $fn = 24);
    }
}

module prop_disc() { color("orange", 0.5) translate([0, 0, z_prop - 1]) cylinder(d = prop_d, h = 2); }
module motor()     { color("gray") cylinder(d = 28, h = prop_to_mount - 12); }   // placeholder body for the picture only

if (part == "duct") duct();
else if (part == "quarter") quarter();
else if (part == "spider") spider();
else if (part == "section") {
    difference() { union() { color("SteelBlue") duct(); color("DimGray") spider(); motor(); }
                   translate([-300, -600, -50]) cube([600, 600, 300]); }
    prop_disc();
}
else { color("SteelBlue") duct(); color("DimGray") spider(); motor(); prop_disc(); }

echo(str("throat diameter ", 2 * throat_r, " mm; highlight diameter ", 2 * highlight_r,
         " mm; outer diameter ", 2 * outer_r, " mm; exit diameter ", 2 * exit_r,
         " mm; exit area / disc area ", pow(exit_r / (prop_d / 2), 2),
         "; lip radius ", 100 * lip_r / (2 * throat_r), " % Dt; diffuser length ", diff_len,
         " mm (", 100 * diff_len / (2 * throat_r), " % Dt); propeller plane at ", z_prop,
         " mm above the exit, ", 100 * (z_top - z_prop) / z_top, " % of the duct length behind the lip; total length ", z_top, " mm"));
