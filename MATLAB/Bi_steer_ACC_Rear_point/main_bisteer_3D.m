%main bisteer 3D
% 11 jun 2024 1:47 PM
clear;
close all;
clc;

restoredefaultpath
addpath("Controller","Dynamics","Graphics");






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
V0 = 1;

psi0 = deg2rad(150);  %heading
phi0 = deg2rad(-10);  %lean angle  -30
phidot0 = 0; %lean rate

theta_F0 = deg2rad(90);  %30
theta_R0 = deg2rad(90); %60
 

z0 = [x0, y0, V0, psi0, phi0, phidot0, theta_F0, theta_R0]';

%%
%

%lqr stuff

ref_phi = [1,deg2rad(0),deg2rad(0)];
Q_phi = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_phi = diag([1e1, 1e2, 1e2]);



ref_V   = [ 0.01,deg2rad(0),deg2rad(0)];
Q_V = diag([1e4, 1e2, 1e4, 1e1 1e1]);
R_V = diag([1e3, 1e2, 1e2]);



ref_1 = [0,deg2rad(89),deg2rad(0)];
Q_F = diag([1e4, 1e2, 1e4, 1e0, 1e0]);
R_F = diag([1e2, 1e1, 1e1]);    %[1e1, 1e1, 1e0, 1e0]

ref_2 = [0.0,deg2rad(10),deg2rad(90)];
%Q_R = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
%R_R = diag([1e2, 1e2, 1e1, 1e1]);
Q_R = diag([1e4, 1e3, 1e4, 1e0, 1e0]);
R_R = diag([1e2, 1e1, 1e1]);



ref_3 = [0.0,deg2rad(10),deg2rad(0)];
Q_3 = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_3 = diag([1e2, 1e1, 1e1]);

ref_4 = [1,deg2rad(0),deg2rad(0)];
Q_4 = diag([1e3, 1e2, 1e3, 1e1, 1e1]);
R_4 = diag([1e2, 1e1, 1e10]);



ref_5 = [0.1,deg2rad(0),deg2rad(0)];
Q_5 = diag([1e3, 1e2, 1e3, 1e1, 1e1]);
R_5 = diag([2e2, 2e1, 1e10]);

ref_6 = [0.01,deg2rad(0),deg2rad(0)];
Q_6 = diag([1e3, 1e2, 1e3, 1e1, 1e1]);
R_6 = diag([3e2, 1e1, 1e10]);

ref_7 = [0.0,deg2rad(89),deg2rad(89)];
Q_R = diag([1e4, 1e3, 1e4, 1e0, 1e0]);
R_R = diag([1e2, 1e1, 1e1]);

ref_8 = [0,deg2rad(89),deg2rad(0)];
Q_8 = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
R_8 = diag([1e2, 1e1, 1e1]); 



p.ref_phi = ref_phi;
p.ref_V   = ref_V;
p.ref_1 = ref_1;
p.ref_2 = ref_2;
p.ref_3 = ref_3;
p.ref_4 = ref_4;
p.ref_5 = ref_5;
p.ref_6 = ref_6;
p.ref_7 = ref_7;
p.ref_8 = ref_8;
Q = diag([1e4, 1e3, 1e4, 1e1, 1e1]);
R = diag([1e0, 1e1, 1e1]);

p.Q = Q;
p.R = R;
%
[K_phi,~,~] = my_lqr(0,z0,p,ref_phi,Q_phi,R_phi);   %z0 not used
[K_V,~,~]  = my_lqr(0,z0,p,ref_V,Q_V,R_V);
[K_1,~,~] = my_lqr(0,z0,p,ref_1,Q_F,R_F)
[K_2,~,~] = my_lqr(0,z0,p,ref_2,Q_R,R_R);
[K_3,~,~] = my_lqr(0,z0,p,ref_3,Q_3,R_3);
[K_4,A,B] = my_lqr(0,z0,p,ref_4,Q_4,R_4);
%rank_4 = rank(ctrb(A,B))

[K_5,A5,B5] = my_lqr(0,z0,p,ref_5,Q_5,R_5);
[K_6,~,~] = my_lqr(0,z0,p,ref_6,Q_R,R_R);
[K_7,~,~] = my_lqr(0,z0,p,ref_7,Q_R,R_R);
[K_8,~,~] = my_lqr(0,z0,p,ref_8,Q_8,R_8);

%rank_5 = rank(ctrb(A5,B5))





p.K_phi     = K_phi;
p.K_V       = K_V;
p.K_1 = K_1;
p.K_2 = K_2;
p.K_3 = K_3;
p.K_4 = K_4;
p.K_5 = K_5;
p.K_6 = K_6;
p.K_7 = K_7;
p.K_8 = K_8;

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
%plot_soln(soln,start,stop,p)

%
tstart = 0;
tend  = stop;
save = 0;
speed = 0.05;
animate_bisteer(soln,tstart,tend,p,speed,save)

%}




