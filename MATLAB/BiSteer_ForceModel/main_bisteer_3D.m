%main bisteer 3D
% 11 jun 2024 1:47 PM
clear;
close all;
clc;

restoredefaultpath
addpath("Controller","Dynamics","Graphics");

theta_dotF0 = 0;
theta_dotR0 = 0;
Tf0=0;
Tr0=0;
t0 =0;


global control0; 

control0 = [theta_dotF0,theta_dotR0,Tf0,Tr0,t0]';

dr = 0.1; df = 0.1;

I11 = 0.01; I22 = 0.01; I33 = 0.01;
m = 2.54;   g = 10;    h = 0.1;

%%
%packing parameters
p = struct();
p.dr = dr; p.df = df;

p.I11 = I11; p.I22 = I22; p.I33 = I33;

p.m = m; p.g = g; p.h = h;

%%
% initial condition
x0 = 0;
y0 = 0;
V0 = 0;

psi0 = deg2rad(0);  %heading
phi0 = deg2rad(10);  %lean angle
phidot0 = 0; %lean rate

theta_F0 = deg2rad(89);  
theta_R0 = deg2rad(88.999);
 

z0 = [x0, y0, V0, psi0, phi0, phidot0, theta_F0, theta_R0]';

%%
%

%lqr stuff

ref_phi = [1,deg2rad(0),deg2rad(0)];
Q_phi = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_phi = diag([1e1, 1e1, 1e1, 1e5]);



ref_V   = [ 0.01,deg2rad(0),deg2rad(0)];
Q_V = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_V = diag([1e3, 1e3, 1e2, 1e2]);



ref_1 = [0,deg2rad(89),deg2rad(88)];
Q_F = diag([1e4, 1e4, 1e4, 1e0, 1e0]);
R_F = diag([5e2, 5e2, 1e1, 1e1]);    %[1e1, 1e1, 1e0, 1e0]

ref_2 = [0.0,deg2rad(89.1),deg2rad(89)];
%Q_R = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
%R_R = diag([1e2, 1e2, 1e1, 1e1]);
Q_R = diag([1e4, 1e3, 1e4, 1e0, 1e0]);
R_R = diag([5e2, 5e2, 1e1, 1e1]);



ref_3 = [0.0,deg2rad(80),deg2rad(80)];
Q_3 = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_3 = diag([1e2, 1e2, 1e1, 1e1]);

ref_4 = [1,deg2rad(0),deg2rad(0)];
Q_4 = diag([1e4, 1e1, 1e4, 1e1, 1e1]);
R_4 = diag([1e2, 1e2, 2e1, 1e3]);



ref_5 = [0,deg2rad(90),deg2rad(60)];
Q_5 = diag([1e4, 1e1, 1e4, 1e1, 1e1]);
R_5 = diag([1e2, 1e2, 2e1, 1e3]);

p.ref_phi = ref_phi;
p.ref_V   = ref_V;
p.ref_1 = ref_1;
p.ref_2 = ref_2;
p.ref_3 = ref_3;
p.ref_4 = ref_4;

Q = diag([1e4, 1e3, 1e4, 1e1, 1e1]);
R = diag([1e0, 1e0, 1e1, 1e1]);

p.Q = Q;
p.R = R;
%
%[K_phi,~,~] = my_lqr(0,z0,p,ref_phi,Q_phi,R_phi);   %z0 not used
%[K_V,~,~]  = my_lqr(0,z0,p,ref_V,Q_V,R_V);
[K_1,~,~] = my_lqr(0,z0,p,ref_1,Q_F,R_F)
[K_2,~,~] = my_lqr(0,z0,p,ref_2,Q_R,R_R);
%[K_3,~,~] = my_lqr(0,z0,p,ref_3,Q_3,R_3);
%[K_4,A,B] = my_lqr(0,z0,p,ref_4,Q_4,R_4);
%rank_4 = rank(ctrb(A,B))

%[K_5,A5,B5] = my_lqr(0,z0,p,ref_5,Q_4,R_5);
%rank_5 = rank(ctrb(A5,B5))





%p.K_phi     = K_phi;
%p.K_V       = K_V;
p.K_1 = K_1;
p.K_2 = K_2;
%p.K_3 = K_3;
%p.K_4 = K_4;
%% LQR stuff
%{
syms Tf Tr theta_Fdot theta_Rdot psi real
syms phi V phidot theta_F theta_R real

mass_A = A(I11,I22,I33,df,dr,h,m,phi,psi,theta_F,theta_R);
force_F =b(I11,I22,I33,Tf,Tr,V,df,dr,g,h,m,phi,phidot,psi0,theta_F,theta_R,theta_Fdot,theta_Rdot);

dots = mass_A\force_F;
Vdot = dots(1);
phiddot = dots(2);


dynamics_lin = [phidot, Vdot, phiddot, theta_Fdot, theta_Rdot];
state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
U            = [    Tf, Tr, theta_Fdot, theta_Rdot];

 
%}


%%
%{
eqn1 = simplify(subs(Vdot,   [phidot,theta_Fdot,theta_Rdot],[0,0,0]));
eqn2 = simplify(subs(phiddot,[phidot,theta_Fdot,theta_Rdot],[0,0,0]));

%

eqn1 = simplify(subs(eqn1,[phi,Tf,Tr],[0.01,0,0]));
eqn2 = simplify(subs(eqn1,[phi,Tf,Tr],[0.01,0,0]));

%matlabFunction([eqn1,eqn2],'File','equb.m',Optimize=true)
fun = @ equb;
theta = [0.1,0.02];

theta=fsolve(fun,theta)

%}



%%

%
%creat a function
therhs = @(t,z) bisteer_3D_rhs(t,z,p);
fall   = @(t,z) bicycle_fall(t,z,p);

%solving parameters
start = 0; stop = 10; t = linspace(start,stop,1000000);

%solve ode
small   = 1e-9;
options = odeset('AbsTol', small, 'RelTol', small, Events=fall);
soln    = ode45(therhs,t, z0,options);



%%
%plotting
%
plot_soln(soln,start,stop,p)

%
tstart = 0;
tend  = stop;
save = 0;
speed = 1;
animate_bisteer(soln,tstart,tend,p,speed,save)

%}




