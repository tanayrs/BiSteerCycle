function [K,A,B] = my_lqr(t,z,p,state_ref,Q,R)

% unpacking parameters
%
I11 = p.I11; 
I22 = p.I22; 
I33 = p.I33; 
m = p.m; 
g = p.g;
h = p.h; 
df = p.df; 
dr = p.dr;
%}


%I11 = 0.01;
%I22 = 0.01;
%I23  = 0.2;
%m =0.01;
%h = 0.02;
%df = 0.12;
%dr = 0.08;

%% equb conditions

phi        = 0;
phidot     = 0;


Tf         = 0;
Tr         = 0;
theta_Fdot = 0;
theta_Rdot = 0;

%% Ref input


Vr       = state_ref(1);
theta_Fr = state_ref(2);
%theta_Fr = sin(t);
theta_Rr = state_ref(3);

psi = deg2rad(70);


%
JF_x = JF_X(I11,I22,I33,Tf,Tr,Vr,df,dr,g,h,m,phi,phidot,psi,theta_Fr,theta_Rr,theta_Fdot,theta_Rdot)
JF_u = JF_U(I22,I33,Vr,df,dr,h,m,phi,psi,theta_Fr,theta_Rr)
M = Mass_matrix_M(I11,I22,I33,df,dr,h,m,phi,theta_Fr,theta_Rr)


A = M\JF_x;
B = M\JF_u;
%}

%A = A_matrix(I11,I22,I33,Tf,Tr,Vr,df,dr,g,h,m,phi,phidot,theta_Fr,theta_Rr,theta_Fdot,theta_Rdot);
%B = B_matrix(I11,I22,I33,Vr,df,dr,h,m,phi,theta_Fr,theta_Rr);


K = lqr(A,B,Q,R);


%{
dynamics_lin = [phidot, Vdot, phiddot, theta_Fdot, theta_Rdot];
state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
U            = [    Tf, Tr, theta_Fdot, theta_Rdot];

%}

end
