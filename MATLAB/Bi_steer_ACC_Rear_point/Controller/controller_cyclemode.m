function [Vfdot,Vdot, theta_Fdot, theta_Rdot] = controller_cyclemode(t,z,p)

persistent prev_error;
persistent prev_t;

    if isempty(prev_error)
        prev_error = 0;
    end

    if isempty(prev_t)
        prev_t = 0;
    end

    dt = t - prev_t;


x   = z(1);
y   = z(2);
V   = z(3);
psi = z(4);
phi = z(5);
phidot = z(6);
theta_F = z(7);
theta_R = z(8);

target_F = -(8*phi + 0.8*phidot);
error    = target_F - theta_F;

theta_Rdot = -5*(error);
theta_Fdot = 10*(error);
disp(dt)

Vdot = 0;
Vfdot = 0;

prev_error = error;
prev_t = t;







end