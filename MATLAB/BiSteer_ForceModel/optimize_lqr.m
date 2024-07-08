%main bisteer 3D

clear;
close all;
clc;

restoredefaultpath
addpath("Controller","Dynamics","Graphics");

dr = 0.1; df = 0.1;

I11 = 0.1; I22 = 0.1; I33 = 0.1;
m = 2.54;   g = 10;    h = 0.2;

%%

%%
%packing parameters
p.dr = dr; p.df = df;

p.I11 = I11; p.I22 = I22; p.I33 = I33;

p.m = m; p.g = g; p.h = h;

%%
% initial condition
x0 = 0;
y0 = 0;
V0 = 0;

psi0 = deg2rad(45);  %heading
phi0 = deg2rad(15);  %lean angle
phidot0 = 0; %lean rate

theta_F0 = deg2rad(90);  
theta_R0 = deg2rad(90);
 
format long
%%

z0 = [x0, y0, V0, psi0, phi0, phidot0, theta_F0, theta_R0]';
p.z0 = z0;
%%

start = 0; stop = 5; t = linspace(start,stop,10000);
p.start = start;
p.stop  = stop;
p.t = t;


c = 1:100;
m = length(c);
n = length(t);

phi     = zeros(n,m);
phidot  = zeros(n,m);
theta_F = zeros(n,m);
theta_R = zeros(n,m);

%%

for i = 1:length(c)

disp('experiment counter')
disp(i)

ref_1 = [0.0,deg2rad(90),deg2rad(90)];
Q_1 = diag([1e4, 1e3, 1e4, 1e1, 1e1]);
R_1 = diag([5*1e2, 5*1e2, c(i)*1e-1, c(i)*1e-1]);
p.ref_1 = ref_1;
[K_1,~,~] = my_lqr(0,z0,p,ref_1,Q_1,R_1);
p.K_1 = K_1;

%{
Q_dynamics_lin = [phidot, Vdot, phiddot, theta_Fdot, theta_Rdot];
ref_state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
R_U            = [    Tf, Tr, theta_Fdot, theta_Rdot];
%}



[success,phi1,phidot1,theta_F1,theta_R1] = experiment(p);

if success == 1
    disp('success')
    disp('')
else
    disp('fail')
    disp('')
end


%disp(c)
if success == 1
    phi(:,i) = phi1;
    phidot(:,i) = phidot1;
    theta_F(:,i) = theta_F1;
    theta_R(:,i) = theta_R1;
end


end

 %% cost function


counter = 1:length(c);
cost_vec = zeros(1,length(counter));

for j = counter

    cost = costfunction(phi(:,j),phidot(:,j),theta_F(:,j),theta_R(:,j));
    cost_vec(j) = cost;


end

for i1 = 1: length(counter)

    if cost_vec(i1) == 999
        cost_vec(i1) = [];
        counter(i1) = [];
    end
end



plot(counter,cost_vec,'r.')

min_cost = min(cost_vec);

for i2 = 1 : length(cost_vec)

    if min_cost == cost_vec(i2)
        min_exp_counter = counter(i2);
    end

end







function cost = costfunction(phi,phidot,theta_F,theta_R)

J1 = phi'*phi;
J2 = phidot'*phidot;

cost = sqrt(J1 + J2);

if cost == 0
    cost = 999;
end
end













