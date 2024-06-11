function [success,phi,phidot,theta_F,theta_R] = experiment(p)



z0 = p.z0;

%creat a function
therhs = @(t,z) bisteer_3D_rhs(t,z,p);
fall   = @(t,z) bicycle_fall(t,z,p);

%solving parameters
start = p.start; stop = p.stop; 


tspan = linspace(start,stop,1000000);

%solve ode
small   = 1e-9;
options = odeset('AbsTol', small, 'RelTol', small, Events=fall);
soln    = ode45(therhs,tspan, z0,options);


t = p.t;

if soln.x(end) ~= stop
    success = 0;
    disp('Event bi_steer fall')
    phi = 0;
    phidot = 0;
    theta_F = 0;
    theta_R =0;
else
    success = 1;
    phi     = deval(soln,t,5)';
    phidot  = deval(soln,t,6)';
    theta_F = deval(soln,t,7)';
    theta_R = deval(soln,t,8)';

end


%z0 = [x0, y0, V0, psi0, phi0, phidot0, theta_F0, theta_R0]';






end