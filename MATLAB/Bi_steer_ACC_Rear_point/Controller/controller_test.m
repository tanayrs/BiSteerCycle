function [Vfdot,Vdot, theta_Fdot, theta_Rdot] = controller_test(t,z,p)

x   = z(1);
y   = z(2);
V   = z(3);
psi = z(4);
phi = z(5);
phidot = z(6);
theta_F = z(7);
theta_R = z(8);



%% control logic
state_ref = [0,1,0,0];
if t > 2 
    %state_ref = [1,0.4*sin(3*(t-1)),0];   %[velocity, front_steer_angle, rear_steer_angle]
    %phi_r      = equb_finder(t,z,p,0.2*sin(2*(t-1)),0);
    phi_r       = equb_finder(t,z,p,deg2rad(20),0);
    state_ref  = [phi_r,1,deg2rad(20),0];
end

K = p.K_test;


%%
phi_r    = state_ref(1);
Vr       = state_ref(2);
theta_Fr = state_ref(3);
theta_Rr = state_ref(4);


error = [  phi_r-phi,    Vr-V,  -phidot,  theta_Fr-theta_F, theta_Rr-theta_R]';
U = K*error;

Vdot = U(1);
Vfdot = (Vdot*(cos(phi)^2 + tan(theta_F)^2)^(1/2))/(cos(phi)^2 + tan(theta_R)^2)^(1/2);

theta_Fdot = U(2);
theta_Rdot = U(3);


end