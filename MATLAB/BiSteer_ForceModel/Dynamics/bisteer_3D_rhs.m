function zdot = bisteer_3D_rhs(t,z,p)

%unpacking state vector z


V       = z(3);
psi     = z(4);
phi     = z(5);
phidot  = z(6);

%rem(t,interval_noise)

%unpacking parameters

I11 = p.I11; I22 = p.I22; I33 = p.I33; m = p.m; g = p.g;
h = p.h; df = p.df; dr = p.dr;



[Tf, Tr, theta_F, theta_R, theta_Fdot, theta_Rdot] = controller_bisteer3D(t,z,p);

theta_F = z(7);
theta_R = z(8);


%Vdot = 0;
%statedot = Bi_steer_3D_DAE(I11,V,Vdot,df,dr,g,h,m,phi,phidot,psi,theta_F,theta_R,theta_Fdot,theta_Rdot);

%statedot = bi_steer_3D_Dynamics_full(I11,I22,I33,Tf,Tr,V,df,dr,g,h,m,phi,phidot,psi,theta_F,theta_R,theta_Fdot,theta_Rdot);

%mass_matrix_A = A(I11,I22,I33,df,dr,h,m,phi,psi,theta_F,theta_R);
%force_vector_b = b(I11,I22,I33,Tf,Tr,V,df,dr,g,h,m,phi,phidot,psi,theta_F,theta_R,theta_Fdot,theta_Rdot);

[A,b] = A_b(I11,I22,I33,Tf,Tr,V,df,dr,g,h,m,phi,phidot,psi,theta_F,theta_R,theta_Fdot,theta_Rdot);


zdot1 = A\b;
zdot2 = x_y_psi_dots(V,df,dr,phi,psi,theta_F,theta_R);



xdot     = zdot2(1);
ydot     = zdot2(2);
Vdot     = zdot1(1);
psidot   = zdot2(3);
%phidot   =  
phiddot  = zdot1(2);


zdot = [xdot, ydot, Vdot, psidot, phidot, phiddot, theta_Fdot, theta_Rdot]';

%syms I11 I22 I33 Tf Tr V df dr g h m phi phidot psi theta_F theta_R theta_Fdot theta_Rdot real


end