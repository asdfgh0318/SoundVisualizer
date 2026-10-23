// Solid liner strip printed standing on its edge as a flat spiral (like a tape roll), then
// uncoiled into the slot. No ladder: one continuous 0.8 mm wall, 100 mm tall.
// The strip is longer than the slot circumference by `extra`; the surplus overlaps itself
// in the slot so the liner springs outward.
D_in   = 210;    // slot inner diameter, mm
H      = 100;    // slot height = wall height, mm
wall   = 0.8;    // wall thickness (two 0.4 mm perimeters)
extra  = 30;     // added to the circumference (overlap in the slot)
r0     = 30;     // spiral radius at the inner end (centre line), mm
gap    = 4;      // clear space between turns on the bed, mm

L  = PI*(D_in - wall) + extra;     // strip length
p  = wall + gap;                   // spiral pitch per turn
b  = p/(2*PI);                     // r = r0 + b*theta
// arc length of r = r0 + b*theta from 0 to th
function arc(th) = let(u0 = r0/b, u1 = (r0 + b*th)/b)
  (b/2)*((u1*sqrt(u1*u1+1) + asinh_(u1)) - (u0*sqrt(u0*u0+1) + asinh_(u0)));
function asinh_(x) = ln(x + sqrt(x*x+1));
function solve(lo, hi, n=0) = (n > 40) ? (lo+hi)/2 :
  let(m = (lo+hi)/2) (arc(m) < L) ? solve(m, hi, n+1) : solve(lo, m, n+1);
th_end = solve(0, 60);
steps  = ceil(th_end*180/PI/3);    // one point every 3 degrees
function pt(th, d) = let(r = r0 + b*th + d*wall/2) [r*cos(th*180/PI), r*sin(th*180/PI)];
outer = [for (i = [0:steps]) pt(th_end*i/steps, +1)];
inner = [for (i = [steps:-1:0]) pt(th_end*i/steps, -1)];

linear_extrude(H) polygon(concat(outer, inner));
echo(L=L, turns=th_end/(2*PI), outer_diameter=2*(r0 + b*th_end + wall/2));
