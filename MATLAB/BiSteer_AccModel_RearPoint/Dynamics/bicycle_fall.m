function [lean_phi,stop,direction] = bicycle_fall(t,z,p)
phi = z(5);

lean_phi = abs(phi) - pi/2;
stop = 1;
direction = 0;

end