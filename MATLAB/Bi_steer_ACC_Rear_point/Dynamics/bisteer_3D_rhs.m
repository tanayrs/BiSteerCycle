function zdot = bisteer_3D_rhs(t,z,p)

%unpacking state vector z


V       = z(3);
psi     = z(4);
phi     = z(5);
phidot  = z(6);



%unpacking parameters

I11 = p.I11; I22 = p.I22; I33 = p.I33; m = p.m; g = p.g;
h = p.h; df = p.df; dr = p.dr;



[~, Vdot, theta_Fdot, theta_Rdot] = controller_bisteer3D(t,z,p);

theta_F = z(7);
theta_R = z(8);

zdot = lean_heading(I11,I22,I33,V,Vdot,df,dr,g,h,m,phi,phidot,psi,theta_F,theta_R,theta_Fdot,theta_Rdot);

xdot     = zdot(1);
ydot     = zdot(2);


%
if abs(theta_F-theta_R) < deg2rad(0.001)
    psidot = (V*(theta_F - theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));
else
    psidot = (V*(tan(theta_F) - tan(theta_R)))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));
end
%}


phiddot  = zdot(4);

disp(phiddot)


zdot = [xdot, ydot, Vdot, psidot, phidot, phiddot, theta_Fdot, theta_Rdot]';

%syms I11 I22 I33 Tf Tr V df dr g h m phi phidot psi theta_F theta_R theta_Fdot theta_Rdot real


end