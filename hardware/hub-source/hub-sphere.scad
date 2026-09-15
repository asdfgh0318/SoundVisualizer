// Hub loudspeaker enclosure — 1 litre sealed sphere for a Visaton FRS 8 M.
//
// Built for campaign session 2 (arc flat, source at the propeller hub, sweep +
// tones, motor off). Sealed on purpose: a port is a second, delayed, ringing
// source and the analysis reads echo arrival times straight off each mic's
// impulse response — 1.98 ms at -72 deg, 4.37 ms at +36/+54 deg. The source's
// own decay has to be over before those.
//
// Spherical because we are printing: a doubly-curved shell is far stiffer than
// flat panels of the same thickness, and it has no edges to diffract. The
// driver fires +Z, which is "up" in use, along the rig's vertical axis.
//
// Render one half at a time:
//   openscad -D 'part="bottom"' -o bottom.stl hub-sphere.scad
//   openscad -D 'part="top"'    -o top.stl    hub-sphere.scad
//   part="both" (default) shows the assembly for inspection.

/* [What to build] */
// "onepiece" is the intended build: a single shell whose only opening is the
// driver cutout, printed with that flat face on the bed. "top"/"bottom" are the
// older split-at-the-equator version, kept because it needs no bridging at all.
part = "onepiece";      // "onepiece", "section", "top", "bottom", "both"
orient_for_print = true; // onepiece only: lay the driver flat on z=0, opening down

/* [Acoustic] */
volume_l    = 1.0;      // NET air volume the driver sees, litres -> FRS 8 M: Fc 181 Hz, Qtc 0.71
wall        = 5.0;      // shell wall thickness, mm
driver_displacement_ml = 20; // air the cone/magnet occupies; measure or take from the datasheet
stuffing_g  = 10;       // polyester, loose — not modelled, just a reminder

/* [Driver — Visaton FRS 8 M, Art. 2001, datasheet drawing dated 27.07.2018] */
// Frame is a 78 mm SQUARE with corner tabs, 93 mm across the diagonal; screws on
// an 83 mm bolt circle through 4.5 x 5.5 slots; cut-out 75 mm; overall depth 47 mm
// with a 2.1 mm flange. The seating flat therefore has to clear 93 mm, not the
// ~80 mm a round 8 cm driver would suggest.
driver_cutout_d = 75.0;
driver_frame_across = 93.0; // corner-to-corner, the number the flat must beat
driver_flat_d   = 98.0;     // seating face = frame diagonal + 5 mm of landing
driver_depth    = 47.0;     // for the clearance echo below
gasket_rebate   = 0.0;      // set e.g. 2.5 to recess the flange flush
land_t          = 8.0;      // thickness of the baffle land behind the seating face.
                            // Without it the cavity is WIDER than the bore where the
                            // flat cuts it (opening 83.5 mm against a 75 mm bore), so
                            // the seating face is a 7 mm rim and the screws at the
                            // 83 mm bolt circle land in thin air.
screw_depth     = 6.0;      // BLIND. A through pilot would be four leaks in a box
                            // whose whole point is being sealed.

screw_holes   = true;   // bolt circle is from the drawing, so these are safe now
screw_circle_d = 83.0;
screw_d        = 3.2;   // pilot for a 4 mm self-tapper into plastic; open to 4.3
screw_n        = 4;     // for M4 clearance, or 5.6 for M4 heat-set inserts

/* [Cable + mount] */
cable_d        = 6.0;   // grommet hole, sealed with silicone once wired
cable_z        = -12.0; // onepiece: through the side wall, where it is vertical and
                        // prints as a clean 6 mm bridge. Split build: ignored.
cable_offset   = 25.0;  // split build only: off-axis hole in the bottom cap
mount_boss     = true;  // blind hole for an M6 heat-set insert
mount_insert_d = 8.0;
mount_insert_h = 10.0;
mount_pad_d    = 26.0;
boss_d         = 30.0;  // onepiece: solid CONE at the apex, so the insert goes into solid
boss_h         = 24.0;  // material. A cone, not a cylinder: printed flat-face-down the
                        // apex is the highest point, and a cone that widens upward is
                        // self-supporting, where a cylinder would leave its whole
                        // underside as an unsupported island in mid-air.

/* [Print fit] */
lip_h    = 6.0;         // spigot that locates the two halves
fit_clr  = 0.25;        // clearance on the spigot; loosen to 0.35 on a sloppy printer
$fn      = 220;

// ---------------------------------------------------------------- derived
// The driver flat slices a cap off the top of the cavity, and the driver itself
// displaces air, so a sphere sized straight from volume_l comes out small. Both
// losses depend on r_in, so solve for the radius that leaves volume_l behind.
function cap_v(ri, fz) = (ri <= fz) ? 0
    : PI * pow(ri - fz, 2) * (3 * ri - (ri - fz)) / 3;
// The apex plug eats into the cavity by whatever of boss_h reaches past the wall.
// Only the part of the cone past the wall steals cavity volume. At depth `wall`
// from the base the cone radius is rb, and what intrudes is a cone of height
// boss_h - wall on that radius.
function boss_v(ri) = (part != "onepiece" || !mount_boss) ? 0
    : PI * pow(boss_d / 2 * (1 - wall / boss_h), 2) * (boss_h - wall) / 3;
// The land fills the cavity from the bore out to the wall over land_t of height.
// No closed form worth writing, so integrate it in slices.
function cav_r(ri, z) = (abs(z) >= ri) ? 0 : sqrt(ri * ri - z * z);
function land_slice(ri, z, dz) =
    let (cr = cav_r(ri, z))
    (cr <= driver_cutout_d / 2) ? 0 : PI * (cr * cr - pow(driver_cutout_d / 2, 2)) * dz;
function land_sum(ri, fz, i, n) =
    let (dz = land_t / n)
    (i >= n) ? 0
    : land_slice(ri, fz - land_t + (i + 0.5) * dz, dz) + land_sum(ri, fz, i + 1, n);
function land_v(ri) = (part != "onepiece") ? 0
    : land_sum(ri, sqrt(pow(ri + wall, 2) - pow(driver_flat_d / 2, 2)), 0, 48);

function net_v(ri) =
    4 / 3 * PI * pow(ri, 3)
    - cap_v(ri, sqrt(pow(ri + wall, 2) - pow(driver_flat_d / 2, 2)))
    - boss_v(ri)
    - land_v(ri)
    - driver_displacement_ml * 1000;
// Bisection: plain, converges, and OpenSCAD has no solver of its own.
function solve_r(lo, hi, target, n) =
    (n <= 0) ? (lo + hi) / 2
    : (net_v((lo + hi) / 2) > target ? solve_r(lo, (lo + hi) / 2, target, n - 1)
                                     : solve_r((lo + hi) / 2, hi, target, n - 1));

r_in  = solve_r(40, 110, volume_l * 1e6, 40);
r_out = r_in + wall;
// Height of the plane that cuts a flat of driver_flat_d across the outer sphere.
flat_z = sqrt(pow(r_out, 2) - pow(driver_flat_d / 2, 2));

echo(str("internal radius  ", r_in,  " mm  (dia ", 2 * r_in,  ")"));
echo(str("external radius  ", r_out, " mm  (dia ", 2 * r_out, ")"));
echo(str("driver flat at z ", flat_z, " mm, flat dia ", driver_flat_d));
echo(str("net air volume   ", net_v(r_in) / 1000, " ml  (target ", volume_l * 1000, ")"));
echo(str("flat clears frame diagonal by ", (driver_flat_d - driver_frame_across) / 2, " mm per side"));
echo(str("driver protrudes to z = ", flat_z - (driver_depth - 2.1),
         " mm; cavity floor at ", -r_in, " mm"));
echo(str("seating face ", driver_cutout_d, " to ", driver_flat_d, " mm = ",
         (driver_flat_d - driver_cutout_d) / 2, " mm wide (also the first layer)"));
echo(str("cavity would open to ", 2 * sqrt(max(pow(r_in,2) - pow(flat_z,2), 0)),
         " mm without the land; screws sit at ", screw_circle_d, " mm"));
echo(str("screw pilots ", screw_depth, " mm deep into a ", land_t,
         " mm land -> ", land_t - screw_depth, " mm of material left, blind"));
echo(str("overhang at the bed ", asin((driver_flat_d / 2) / r_out), " deg from vertical"));

module shell() {
    difference() {
        sphere(r = r_out);
        sphere(r = r_in);
    }
}

module driver_flat_cut() {
    // Everything above the seating plane goes away, leaving a flat annulus.
    translate([0, 0, flat_z]) cylinder(h = r_out, r = r_out + 1);
}

// Solid ring behind the seating face, so the face is a full bore-to-flat annulus
// and the mounting screws have something to bite.
module driver_land() {
    intersection() {
        sphere(r = r_out);
        difference() {
            translate([0, 0, flat_z - land_t]) cylinder(h = land_t, d = driver_flat_d);
            translate([0, 0, flat_z - land_t - 1]) cylinder(h = land_t + 2, d = driver_cutout_d);
        }
    }
}

module driver_bore() {
    translate([0, 0, -1]) cylinder(h = r_out + 2, d = driver_cutout_d);
    if (gasket_rebate > 0)
        translate([0, 0, flat_z - gasket_rebate])
            cylinder(h = gasket_rebate + 1, d = driver_flat_d + 0.4);
    if (screw_holes)
        for (i = [0 : screw_n - 1])
            rotate([0, 0, i * 360 / screw_n])
                translate([screw_circle_d / 2, 0, flat_z - screw_depth])
                    cylinder(h = screw_depth + 1, d = screw_d);
}

module cable_hole() {
    translate([cable_offset, 0, -r_out - 1]) cylinder(h = r_out + 2, d = cable_d);
}

module mount() {
    // Pad flattened onto the south pole, with a solid plug behind it so the
    // insert never breaks into the sealed volume.
    difference() {
        union() {
            intersection() {
                sphere(r = r_out);
                translate([0, 0, -r_out])
                    cylinder(h = r_out - r_in + mount_insert_h + 3, d = mount_pad_d);
            }
            translate([0, 0, -r_out]) cylinder(h = 3, d = mount_pad_d);
        }
        translate([0, 0, -r_out - 0.1])
            cylinder(h = mount_insert_h + 0.1, d = mount_insert_d);
    }
}

// Spigot: the inner half of the wall continues up from the equator on the
// bottom part; the top part is hollowed out to the same radius to receive it.
module lip_solid() {
    difference() {
        cylinder(h = lip_h, r = r_in + wall / 2 - fit_clr);
        translate([0, 0, -1]) cylinder(h = lip_h + 2, r = r_in);
    }
}

module lip_pocket() {
    difference() {
        cylinder(h = lip_h + fit_clr, r = r_in + wall / 2);
        translate([0, 0, -1]) cylinder(h = lip_h + 2 + fit_clr, r = r_in - 0.001);
    }
}

module bottom_half() {
    difference() {
        union() {
            intersection() {
                shell();
                translate([0, 0, -r_out - 1]) cylinder(h = r_out + 1, r = r_out + 1);
            }
            lip_solid();
            if (mount_boss) mount();
        }
        cable_hole();
        if (mount_boss)
            translate([0, 0, -r_out - 0.1]) cylinder(h = mount_insert_h + 0.1, d = mount_insert_d);
    }
}

module top_half() {
    difference() {
        intersection() {
            shell();
            translate([0, 0, 0]) cylinder(h = r_out + 1, r = r_out + 1);
        }
        driver_flat_cut();
        driver_bore();
        lip_pocket();
    }
}

module apex_plug() {
    // Solid material filling the shell at the -Z pole, so the M6 insert has
    // something to bite into and the printed dome closes to a point instead of
    // bridging a flat cap.
    intersection() {
        sphere(r = r_out);
        translate([0, 0, -r_out - 0.1]) cylinder(h = boss_h + 0.1, d1 = boss_d, d2 = 0);
    }
}

module side_cable_hole() {
    translate([0, 0, cable_z]) rotate([0, 90, 0])
        cylinder(h = r_out + 2, d = cable_d);
}

module one_piece() {
    difference() {
        union() {
            shell();
            driver_land();
            if (mount_boss) apex_plug();
        }
        driver_flat_cut();
        driver_bore();
        side_cable_hole();
        if (mount_boss)
            translate([0, 0, -r_out - 0.1])
                cylinder(h = mount_insert_h + 0.1, d = mount_insert_d);
    }
}

module one_piece_oriented() {
    if (orient_for_print) translate([0, 0, flat_z]) rotate([180, 0, 0]) one_piece();
    else one_piece();
}

if (part == "onepiece") one_piece_oriented();
else if (part == "bottom") bottom_half();
else if (part == "top") top_half();
else if (part == "section")
    difference() {
        if (true) { one_piece(); }
        translate([0, -r_out - 5, -r_out - 5]) cube([r_out + 10, r_out + 10, 2 * r_out + 10]);
    }
else { bottom_half(); top_half(); }
