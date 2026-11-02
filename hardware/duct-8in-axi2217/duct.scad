// Pusher duct for the APC 8x4.5MR(P) on the AXI 2217/12, one piece with the motor on the Tyto 1585 stand.
// Geometry follows docs/acoustic-speculations/duct-inlet-design-rules.pdf (derived from the
// verified extracts in the papers repo): ~1 mm tip gap, lip radius ~12 % of the throat diameter,
// wall >= 10 % of D at the propeller plane, propeller well behind the lip, 10 deg diffuser,
// exit area ratio 1.1-1.3, supports well clear of the rotor.
//
// Pusher layout: air enters at the top (inlet lip), passes the stand plate, the hub and the
// three aerofoil struts and the motor, then the propeller, then leaves through the diffuser at
// the bottom. The motor hangs from the hub with its shaft pointing down to the propeller; the
// Tyto motor plate bolts onto the hub from upstream, on the same bolts as the motor.
// Thrust pushes the duct towards the stand, so it reads with the opposite sign to a tractor.
// Needs a pusher propeller (APC 8x4.5MRP) or the motor reversed with the propeller flipped.
//
// z = 0 is the exit (flat face, print the duct quarters on it).
//   openscad -D 'part="quarter"' -o duct_quarter.stl duct.scad   // print 4x, pin + glue
//   openscad -D 'part="duct"'    -o duct_full.stl    duct.scad   // whole ring (~265 mm)
//   openscad -D 'part="spider"'  -o spider.stl       duct.scad   // hub + 3 aerofoil struts, printed flat

part = "assembly";   // duct | quarter | spider | assembly

// ---- propeller and gap ----
prop_d    = 203.2;   // APC 8x4.5MR(P), 8 in
tip_gap   = 1.0;     // rule 1: as small as can be built; check the real gap with a feeler gauge
throat_r  = prop_d / 2 + tip_gap;
blade_below = 10;    // straight throat below the disc, covers the blade tips' axial extent [MEASURE]

// ---- inlet ----
lip_r     = 25;      // rule 2: ~12 % of throat diameter (6 % minimum = 12 mm)
lip_out_r = 5;
wall      = 30;      // rule 3: >= 0.1 * prop_d = 20 mm at the propeller plane

// ---- motor stack (MEASURE these before printing) ----
prop_to_mount   = 55;    // propeller disc to the motor's rear mounting face, mm   [MEASURE]
mount_holes_n   = 4;     // AXI 2217 rear mount                                    [MEASURE]
mount_holes_pcd = 25;    // hole circle diameter                                   [MEASURE]
mount_hole_d    = 3.2;   // M3 clearance; long M3 bolts go stand plate -> hub -> motor
hub_hole_d      = 12;    // clearance for the shaft end / circlip / bearing boss   [MEASURE]

// ---- outlet ----
diff_angle = 10;                              // rule 5
diff_len   = 45;                              // exit area ratio ~1.18 at 10 deg
exit_r     = throat_r + diff_len * tan(diff_angle);
outer_exit_r = exit_r + 14.5;

// ---- hub and struts (upstream of the propeller) ----
hub_r      = 22;
hub_t      = 22;     // = strut_chord, so hub and struts print flat on the motor-side face
struts_n   = 3;       // odd, so the two blades never pass two struts at once
strut_chord = 22;     // along the flow
strut_tc   = 0.15;    // NACA 0015 section
root_w     = 8;       // thickened root that carries the M3 heat-set insert
root_len   = 12;      // radial length of the thickened root
pocket     = 3;       // root sits this deep in the duct wall
insert_d   = 4.0;     // M3 heat-set insert
insert_depth = 8;
screw_d    = 3.4;
cbore_d    = 6.5;     // counterbore for the screw head, from the outside of the duct
strut_angle0 = 45;    // keeps the struts off the quarter cut planes (0/90/180/270)

// ---- quarter split ----
pin_d     = 3.2;
pin_depth = 8;

$fn = 180;

z_prop   = diff_len + blade_below;
z_hub0   = z_prop + prop_to_mount;               // motor rear face = hub's downstream face
z_strut  = z_hub0 + strut_chord / 2;             // strut mid-chord; struts flush with the hub
z_lip0   = z_strut + strut_chord / 2 + 5;        // straight throat ends above the struts
z_top    = z_lip0 + lip_r;
highlight_r = throat_r + lip_r;
outer_r  = throat_r + wall;

function arc(c, r, a0, a1, n = 24) = [for (i = [0:n]) let(a = a0 + (a1 - a0) * i / n) [c[0] + r * cos(a), c[1] + r * sin(a)]];
function naca_half(c, t, n = 30) = [for (i = [0:n]) let(x = (1 - cos(180 * i / n)) / 2)
    [x * c, 5 * t * c * (0.2969 * sqrt(x) - 0.1260 * x - 0.3516 * x * x + 0.2843 * pow(x, 3) - 0.1036 * pow(x, 4))]];
function naca(c, t) = let(h = naca_half(c, t)) concat(h, [for (i = [len(h) - 2:-1:1]) [h[i][0], -h[i][1]]]);

profile = concat(
    [[exit_r, 0], [throat_r, diff_len], [throat_r, z_lip0]],
    arc([highlight_r, z_lip0], lip_r, 180, 90),
    arc([highlight_r, z_top - lip_out_r], lip_out_r, 90, 0),
    [[outer_r, z_prop], [outer_exit_r, 0]]
);

assert(highlight_r + lip_out_r >= outer_r - 0.01, "lip and wall do not meet; raise lip_r or lower wall");
assert(wall >= 0.1 * prop_d, "rule 3: wall thinner than 10 % of the propeller diameter");
assert(z_strut - strut_chord / 2 - z_prop >= 0.055 * 2 * throat_r, "rule 6: struts closer than ~5.5 % Dt to the disc");

module at_struts() { for (i = [0:struts_n - 1]) rotate([0, 0, strut_angle0 + i * 360 / struts_n]) children(); }

module duct() {
    difference() {
        rotate_extrude() polygon(profile);
        at_struts() {
            translate([throat_r - 0.01, -root_w / 2 - 0.3, z_strut - strut_chord / 2 - 0.3])
                cube([pocket + 0.01, root_w + 0.6, strut_chord + 0.6]);                  // root pocket
            translate([throat_r, 0, z_strut]) rotate([0, 90, 0]) cylinder(d = screw_d, h = wall + 10, $fn = 24);
            translate([throat_r + 8, 0, z_strut]) rotate([0, 90, 0]) cylinder(d = cbore_d, h = wall + 10, $fn = 32);
        }
    }
}

module quarter() {
    pin_rs = [throat_r + 0.3 * wall, throat_r + 0.7 * wall];
    pin_zs = [diff_len / 2 + 5, z_prop + 20, z_lip0 - 10];
    difference() {
        intersection() { duct(); translate([0, 0, -1]) cube([400, 400, 400]); }
        for (r = pin_rs, z = pin_zs) {
            translate([r, 0, z]) rotate([-90, 0, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
            translate([0, r, z]) rotate([0, 90, 0]) cylinder(d = pin_d, h = 2 * pin_depth, center = true, $fn = 24);
        }
    }
}

// Hub and struts in place (z = hub's downstream face at z_hub0).
module spider() {
    difference() {
        union() {
            translate([0, 0, z_hub0]) cylinder(r = hub_r, h = hub_t);
            at_struts() {
                // aerofoil strut: chord along z, thickness tangential, extruded radially
                translate([hub_r - 3, 0, z_strut + strut_chord / 2]) rotate([0, 90, 0])
                    linear_extrude(throat_r + pocket - 0.3 - (hub_r - 3)) rotate([0, 0, 0]) polygon(naca(strut_chord, strut_tc));
                hull() {                                   // thickened root carrying the insert
                    translate([throat_r - root_len, -strut_tc * strut_chord / 2, z_strut - strut_chord / 2]) cube([0.1, strut_tc * strut_chord, strut_chord]);
                    translate([throat_r - 4, -root_w / 2, z_strut - strut_chord / 2]) cube([4 + pocket - 0.3, root_w, strut_chord]);
                }
            }
        }
        translate([0, 0, z_hub0 - 1]) cylinder(d = hub_hole_d, h = hub_t + 2);
        for (i = [0:mount_holes_n - 1]) rotate([0, 0, 45 + i * 360 / mount_holes_n])
            translate([mount_holes_pcd / 2, 0, z_hub0 - 1]) cylinder(d = mount_hole_d, h = hub_t + 2, $fn = 24);
        at_struts() translate([throat_r + pocket - 0.3 - insert_depth, 0, z_strut]) rotate([0, 90, 0]) cylinder(d = insert_d, h = insert_depth + 1, $fn = 24);
    }
}

module prop_disc() { color("orange", 0.5) translate([0, 0, z_prop - 1]) cylinder(d = prop_d, h = 2); }
module motor()     { color("gray") translate([0, 0, z_prop + 12]) cylinder(d = 28, h = prop_to_mount - 12); }   // placeholder body
module stand()     { color("DimGray", 0.6) translate([-20, -20, z_hub0 + hub_t]) cube([40, 40, 4]); }           // Tyto motor plate, placeholder

if (part == "duct") duct();
else if (part == "quarter") quarter();
else if (part == "spider") translate([0, 0, -z_hub0]) spider();
else { color("SteelBlue") duct(); color("DimGray") spider(); motor(); stand(); prop_disc(); }

echo(str("throat diameter ", 2 * throat_r, " mm; outer diameter ", 2 * outer_r,
         " mm; exit diameter ", 2 * exit_r, " mm; exit area / disc area ", pow(exit_r / (prop_d / 2), 2),
         "; lip radius ", 100 * lip_r / (2 * throat_r), " % Dt; propeller ", z_top - z_prop,
         " mm below the lip edge (", 100 * (z_top - z_prop) / z_top, " % of the length); struts ",
         z_strut - strut_chord / 2 - z_prop, " mm upstream of the disc (", 100 * (z_strut - strut_chord / 2 - z_prop) / (2 * throat_r),
         " % Dt); total length ", z_top, " mm"));
