%derives nonlinear EQM for bisteer cycle : analysis about rear ground
%contact point

%creater       : Vishvas Gajera at Ruina LAB IISc
%Last Modified : 12 Jun 11:18 PM


clc
clear

restoredefaultpath;

syms m I11 I22 I33 positive
syms dr df h positive


syms kf kr positive

syms    x    y    psi    phi    theta_R    theta_F real
syms xdot ydot psidot phidot theta_Rdot theta_Fdot real

syms Tr   Tf                         real
syms V  Vdot vFscalar  Vf Vfdot      real
syms Nf Nr Nfg Nrg g                 real 
syms phiddot psiddot                 real


assumeAlso((phi > -pi/2 ) & (phi < pi/2))

%{
assumeAlso((theta_F ~= theta_R) & (theta_R ~= theta_F))
assumeAlso(tan(theta_F) ~= tan(theta_R))
assumeAlso(cos(theta_F)*sin(theta_R) ~= cos(theta_R)*sin(theta_F))
assumeAlso((theta_F <= pi) & (theta_F>=-pi))
assumeAlso(theta_R <=pi & theta_R>=-pi)
assumeAlso(theta_F ~= pi/2 & theta_F ~= -pi/2)
assumeAlso(theta_R ~= pi/2 & theta_R ~= -pi/2)
%}
%assumeAlso(theta_R ~= -theta_F)
%assume(~in(psi/pi, 'integer') & ~in(phi/pi - 1/2, 'integer'))




state    = [   x,    y,    V,    psi,  psidot,     phi,   phidot,    theta_R,    theta_F];
statedot = [xdot, ydot, Vdot, psidot, psiddot,  phidot,  phiddot, theta_Rdot, theta_Fdot];


zdot =     [xdot, ydot, Vdot, psidot,       5,       6,  phiddot,          8,          9]';

%%

i = [1,0,0]'; 
j = [0,1,0]'; 
k = [0,0,1]';

a1 =  cos(psi)*i + sin(psi)*j;
a2 = -sin(psi)*i + cos(psi)*j;
a3 =  k;


%% Body frame
b1 =  a1;
b2 =  cos(phi)*a2 + sin(phi)*k;
b3 = -sin(phi)*a2 + cos(phi)*k;


%% front wheel frame
f1 =  cos(theta_F)*b1 + sin(theta_F)*b2;
f2 = -sin(theta_F)*b1 + cos(theta_F)*b2;
f3 = b3;


%% rear wheel frame
r1 =  cos(theta_R)*b1 + sin(theta_R)*b2;
r2 = -sin(theta_R)*b1 + cos(theta_R)*b2;
r3 = b3;

%% wheel ground track 
%
%f_track  = cross(f2,k);
%{
norm_f   = simplify(norm(f_thred),"IgnoreAnalyticConstraints",true);
f_thred  = f_thred/norm_f;
%f_thred  = f_thred/norm(f_thred);



%tan(alpha_F) = tan(theta_F)/cos(phi);

%f_thred  = cos(alpha_F)*a1 + sin(alpha_F)*a2;

%}

%
f_track =  [cos(phi)*cos(psi) - tan(theta_F)*sin(psi);
            cos(phi)*sin(psi) + tan(theta_F)*cos(psi);0]/(sqrt(cos(phi)^2 + tan(theta_F)^2));

%}

f_constr = cross(k,f_track);

%
%r_track  = cross(r2,k);
%{
norm_r   = simplify(norm(r_thred),'IgnoreAnalyticConstraints',true);
r_thred  = r_thred/norm_r;
%}
%r_thred  = r_thred/norm(r_thred);

%alpha_R = real(atan(tan(theta_R)/cos(phi)));

%tan(alpha_R) = tan(theta_R)/cos(phi);

%r_thred = cos(alpha_R)*a1 + sin(alpha_R)*a2;

%
r_track  = [cos(phi)*cos(psi) - tan(theta_R)*sin(psi);
            cos(phi)*sin(psi) + tan(theta_R)*cos(psi);0]/(sqrt(cos(phi)^2 + tan(theta_R)^2));
%}


r_constr = cross(k,r_track);


%inertia tensor
IG = [I11,   0, 0;
        0, I22, 0;
        0,   0, I33];


%inertia tensor is along the princple body axis
%needs to be transformed into the inertial frame of refrance to write
%dynamics in inertial frame
B=[b1,b2,b3];   %warning same var name B is body frame %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
IG = B*IG*B';
IG = simplify(IG);


%%

rGrelR =          dr*a1 + h*b3;
rFrelR =     (dr+df)*a1;
rFrelG =          df*a1 - h*b3;

rGrelF = -rFrelG;
rRrelF = -rFrelR;

omega  = psidot*k + phidot*a1;
vR     = V*r_track;

xdot   = vR(1);
ydot   = vR(2);



%%
%%%%%%%%%%%%%%%%calculation to find psiddot%%%%%%%%%%%%%%%%%%%%%
%psiddot depends on front vF and vR


%side calculation to find vf

vFa     = vR + cross(omega,rFrelR);  %front point velocity from rear veocity
%vFa     = simplify(vFa);              
%
vFb     = vFscalar*f_track;               %front point velocity from skate constraint


eqn1    = dot(vFa-vFb,i);
eqn2    = dot(vFa-vFb,j);
eqn    = dot(vFa,f_constr);
eqns    = [eqn1, eqn2];

psidot1 = solve(eqn,psidot);
psidot1 = simplify(psidot1);

sol = solve(eqns,[psidot,vFscalar]);  %solving eqns to find heading rate and vF


psidot = sol.psidot;
vFscalar = sol.vFscalar;


psidot            = simplify(psidot)
vFscalar          = simplify(vFscalar);

vF                = vFscalar*f_track;
vF                = simplify(vF);




psiddot           = jacobian(psidot,state)*statedot';  %psiddot in terms of Vdot, theta_F, theta_R
psiddot           = simplify(psiddot);

%}

%% %%%%%%%%%calculation to find accleration of CG

%

omega  = subs(omega);

vGrelR = cross(omega,rGrelR);
vG     = vR + vGrelR;
%vG     = subs(vG);
vG     = simplify(vG);

%%
syms aFscalar real

aR = jacobian(vR,state)*statedot';
aF = jacobian(vF,state)*statedot';



vGrelR = cross(omega,rGrelR);
aGrelR = jacobian(vGrelR,state)*statedot';

vGrelF = cross(omega,rGrelF);
aGrelF     = jacobian(vGrelF,state)*statedot';


%%

%

aG     = aR + aGrelR;
%aG1    = aF + aGrelF;
aG     = subs(aG);   %substitute psidot in aG new aG in terms of theta_R F
aG     = simplify(aG);


alpha   = jacobian(omega,state)*statedot';  % omega cross omega =0

%%%%%%above this line all seems correct and checked 23 feb 2024

%}

%%
%

%%
%%%%%%%%%%%%matlabfunction to create a function file from formula

%statedot = subs(statedot);

%matlabFunction(statedot,'File','Bi_steer_3D_DAE.m','Optimize',true);

%%

%}

%linear momentum balance about cg 
%

LMB_CG = Tf*f_track + Nf*f_constr + Tr*r_track + Nr*r_constr + Nfg*k + Nrg*k -m*g*k - m*aG;

%angular momentum balance about fromt point

%bottom part requires attension EQN3
%

M_F    =     cross(rRrelF, Nr*r_constr) + cross(rRrelF,Tr*r_track)...
          +  cross(rGrelF,-m*g*k) + cross(rRrelF,Nrg*k) ;


H_dot_F = cross(rGrelF,aG*m) + IG*alpha + cross(omega,IG*omega);

%{
M_R    =    cross(rFrelR, Nf*f2)  + cross(rFrelR,Tf*f1)...
         +  cross(rGrelR,-m*g*k)  + cross(rFrelR,Nfg*k);

H_dot_R = cross(rGrelR,aG)*m  + IG*alpha;
%}




AMB_F   = M_F - H_dot_F;
AMB_F   = simplify(AMB_F);
%{
AMB_R   = M_R - H_dot_R;
AMB_R   = simplify(AMB_R);
%}

%%
%{
EQN1 = dot(LMB_CG,a1);
EQN1 = subs(EQN1);
%EQN1 = simplifyFraction(EQN1);
EQN1 = simplify(EQN1);

disp('1 done')


%%
tic
EQN2 = dot(LMB_CG,a2);
EQN2 = subs(EQN2);
%EQN2 = simplifyFraction(EQN2);
EQN2 = simplify(EQN2);
toc
disp('2 done')

%[Nf,Nr] = solve([EQN1,EQN2],[Nf,Nr]);
sol1 = solve([EQN1,EQN2],[Nf,Nr],"ReturnConditions",true);
Nf = simplify(sol1.Nf);
Nr = simplify(sol1.Nr);

%}

%%
tic
EQN4 = dot(AMB_F,a1);
EQN4 = subs(EQN4);
%EQN4 = simplifyFraction(EQN4);
EQN4 = simplify(EQN4,"IgnoreAnalyticConstraints",true,Steps=100);
toc
disp('4 done')
%%


sol = solve(EQN4,phiddot,'ReturnConditions',true);
phiddot = subs(sol.phiddot);
phiddot = simplify(phiddot,'IgnoreAnalyticConstraints',true,Steps=1000);


%% front rear acc vdot stuff
%{


EQN6 = dot(V*r_track,a1) - dot(Vf*f_track,a1);
EQN6 = simplify(EQN6);

EQN7 = dot(Vdot*r_track,a1) - dot(Vfdot*f_track,a1);
EQN7 = simplify(EQN7);

Vf    = solve(EQN6,Vf);
Vfdot = solve(EQN7,Vfdot);

Vf    = simplify(Vf);
Vfdot = subs(Vfdot);
Vfdot = simplify(Vfdot,'IgnoreAnalyticConstraints',true,Steps=1000);

%}


%{


zdot = [xdot,ydot,psidot,phiddot]';




%
dynamics_lin = [phidot, Vdot, phiddot, theta_Fdot, theta_Rdot]';
state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
U            = [ Vdot, theta_Fdot, theta_Rdot];

%%


%A_lin = jacobian(dynamics_lin,state_lin);
%B_lin = jacobian(dynamics_lin,U);

%matlabFunction(zdot,'File','lean_heading.m','Optimize',true);
%matlabFunction(A_lin,'File','A_matrix.m','Optimize',true);
%matlabFunction(B_lin,'File','B_matrix.m','Optimize',true);

%}

