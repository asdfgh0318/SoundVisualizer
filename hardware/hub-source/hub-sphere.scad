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
part = "both";          // "top", "bottom", "both", "section"

/* [Acoustic] */
volume_l    = 1.0;      // NET air volume the driver sees, litres -> FRS 8 M: Fc 181 Hz, Qtc 0.71
wall        = 5.0;      // shell wall thickness, mm
driver_displacement_ml = 20; // air the cone/magnet occupies; measure or take from the datasheet
stuffing_g  = 10;       // polyester, loose — not modelled, just a reminder

/* [Driver — VERIFY AGAINST THE UNIT IN YOUR HAND] */
driver_cutout_d = 75.0; // datasheet cutout for the FRS 8 M
driver_flat_d   = 88.0; // flat seating face; must clear the frame (~80 mm) + gasket
gasket_rebate   = 0.0;  // set e.g. 1.5 to recess the frame flush

screw_holes   = false;  // leave false and drill after measuring the real frame
screw_circle_d = 92.0;
screw_d        = 3.5;
screw_n        = 4;

/* [Cable + mount] */
cable_d        = 6.0;   // grommet hole, sealed with silicone on assembly
cable_offset   = 25.0;  // off-axis, so the south pole is free for the mount
mount_boss     = true;  // pad + blind hole for an M6 heat-set insert
mount_insert_d = 8.0;
mount_insert_h = 10.0;
mount_pad_d    = 26.0;

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
function net_v(ri) =
    4 / 3 * PI * pow(ri, 3)
    - cap_v(ri, sqrt(pow(ri + wall, 2) - pow(driver_flat_d / 2, 2)))
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

module driver_bore() {
    translate([0, 0, -1]) cylinder(h = r_out + 2, d = driver_cutout_d);
    if (gasket_rebate > 0)
        translate([0, 0, flat_z - gasket_rebate])
            cylinder(h = gasket_rebate + 1, d = driver_flat_d + 0.4);
    if (screw_holes)
        for (i = [0 : screw_n - 1])
            rotate([0, 0, i * 360 / screw_n])
                translate([screw_circle_d / 2, 0, flat_z - wall - 2])
                    cylinder(h = wall + 4, d = screw_d);
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

if (part == "bottom") bottom_half();
else if (part == "top") top_half();
else if (part == "section")
    difference() {
        union() { bottom_half(); top_half(); }
        translate([0, -r_out - 5, -r_out - 5]) cube([r_out + 10, r_out + 10, 2 * r_out + 10]);
    }
else { bottom_half(); top_half(); }
