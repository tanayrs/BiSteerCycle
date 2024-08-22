function eqb_state = equb_finder(t,z,p,theta_Fr,theta_Rr)
%% states
V   = z(3);
psi = z(4);
%phi = z(5);
%phidot = z(6);
theta_F = z(7);
theta_R = z(8);

%% params
I11 = p.I11; 
I22 = p.I22; 
I33 = p.I33; 
m = p.m; 
g = p.g;
h = p.h; 
df = p.df; 
dr = p.dr;
%%
theta_Fdot = 0;
theta_Rdot = 0;
Vdot       = 0;

phidot = 0;


%%
phi0 = 0;

fun = @(phi)phiddot(I11,I22,I33,V,Vdot,df,dr,g,h,m,phi,phidot,theta_Fr,theta_Rr,theta_Fdot,theta_Rdot);

phi = fzero(fun,phi0);

eqb_state = phi;
end