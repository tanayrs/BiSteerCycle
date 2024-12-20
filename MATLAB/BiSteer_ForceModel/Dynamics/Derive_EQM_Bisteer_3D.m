clc
clear

syms m I11 I22 I33 positive
syms dr df h positive


syms kf kr positive

syms    x    y    psi    phi    theta_R    theta_F real
syms xdot ydot psidot phidot theta_Rdot theta_Fdot real

syms Tr   Tf                 real
syms V  Vdot vFscalar        real
syms Nf Nr Nfg Nrg g         real 
syms phiddot psiddot         real

syms alpha_F alpha_R real

assumeAlso((phi > -pi/2 ) & (phi < pi/2))
assumeAlso((theta_F ~= theta_R) & (theta_R ~= theta_F))
assumeAlso(tan(theta_F) ~= tan(theta_R))
assumeAlso(cos(theta_F)*sin(theta_R) ~= cos(theta_R)*sin(theta_F))
assumeAlso((theta_F <= pi) & (theta_F>=-pi))
assumeAlso(theta_R <=pi & theta_R>=-pi)
assumeAlso(theta_F ~= pi/2 & theta_F ~= -pi/2)
assumeAlso(theta_R ~= pi/2 & theta_R ~= -pi/2)

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
B=[b1,b2,b3];
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
psidot1 = simplify(psidot1)

sol = solve(eqns,[psidot,vFscalar]);  %solving eqns to find heading rate and vF

%psidot = (tan(theta_F) - tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(1/2);
%psidot = psidot*(V/(df+dr));
%vFscalar = (V*(cos(phi)^2 + tan(theta_F)^2)^(1/2))/(cos(phi)^2 + tan(theta_R)^2)^(1/2);

psidot = sol.psidot;
vFscalar = sol.vFscalar;

%conditions = sol.conditions;
%{
kf = (sin(phi)^2*sin(theta_F)^2 - sin(phi)^2 + 1)^(1/2);
kr = (sin(phi)^2*sin(theta_R)^2 - sin(phi)^2 + 1)^(1/2);
%}

%psidot = subs(psidot);
%vFscalar = subs(vFscalar);



psidot            = simplify(psidot);
vFscalar          = simplify(vFscalar);

vF                = vFscalar*f_track;
vF                = simplify(vF);




psiddot           = jacobian(psidot,state)*statedot';  %psiddot in terms of Vdot, theta_F, theta_R
%psiddot           = simplify(psiddot);

%}

%% %%%%%%%%%calculation to find accleration of CG

%

%omega  = subs(omega);

vGrelR = cross(omega,rGrelR);
vG     = vR + vGrelR;
%vG     = subs(vG);
vG     = simplify(vG);

aR     = jacobian(vR,state)*statedot';
aGrelR = jacobian(vGrelR,state)*statedot';


aG     = aR + aGrelR;
aG     = subs(aG);   %substitute psidot in aG new aG in terms of theta_R F
aG     = simplify(aG);


alpha   = jacobian(omega,state)*statedot';  % omega cross omega =0

%%%%%%above this line all seems correct and checked 23 feb 2024



%%
%{

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
EQN1 = dot(LMB_CG,i);
EQN1 = subs(EQN1);
%EQN1 = simplifyFraction(EQN1);
EQN1 = simplify(EQN1);

disp('1 done')

%%
tic
EQN2 = dot(LMB_CG,j);
EQN2 = subs(EQN2);
%EQN2 = simplifyFraction(EQN2);
EQN2 = simplify(EQN2);
toc
disp('2 done')

%[Nf,Nr] = solve([EQN1,EQN2],[Nf,Nr]);
sol1 = solve([EQN1,EQN2],[Nf,Nr],"ReturnConditions",true);

%Nf = piecewise((theta_F-theta_R ~= 0),sol1.Nf, theta_F-theta_R == 0, 0);
%{
%%
tic
EQN3 = dot(AMB_F,k);
EQN3 = subs(EQN3);
%EQN3 = simplifyFraction(EQN3);
EQN3 = simplify(EQN3);
toc
disp('3 done')

%%
tic
EQN4 = dot(AMB_F,a1);
EQN4 = subs(EQN4);
EQN4 = simplifyFraction(EQN4);
EQN4 = simplify(EQN4);
toc
disp('4 done')
%%
%
tic
EQNS = [EQN3 EQN4];
VARS = [Vdot, phiddot];
toc

%EQNS = subs(EQNS,psi,1);

%sol1 = solve(EQNS,VARS,'IgnoreAnalyticConstraints',true);
%%
%}
%{
[A,b] = equationsToMatrix(EQNS,VARS);

A = simplify(A);
b = simplify(b);
%}
%zdot = [xdot,ydot,Vdot,psidot,phiddot]';

%
%[Vdot, phiddot, Nf, Nr] = vpasolve(EQNS,VARS);

%%
%{
M = [1 ,      0,      0, 0, 0;
     0 , A(1,1), A(1,2), 0, 0;
     0 , A(2,1), A(2,2), 0, 0;
     0 ,      0,      0, 1, 0;
     0 ,      0,      0, 0, 1;];

F = [phidot, b(1), b(2), theta_Fdot, theta_Rdot]';


%%
%matlabFunction(A,'File','A.m','Comments','Mass matrix A','Optimize',true);
%matlabFunction(b,"File",'b.m','Comments','vector_b','Optimize',true);

%%

%matlabFunction([xdot; ydot; psidot],'File','x_y_psi_dots.m','Optimize',true);


%%
%{
xdot   = subs(xdot);
xdot   = simplify(xdot);

ydot   = subs(ydot);
ydot   = simplify(ydot);

Vdot    = subs(Vdot);
%Vdot    = simplify(Vdot);
Vdot    = combine(Vdot,'IgnoreAnalyticConstraints',true);

simplify(Vdot,'Seconds',60,)
%
phiddot = subs(phiddot);
%phiddot = simplify(phiddot);

psidot  = subs(psidot);
psidot  = simplify(psidot);

%psiddot = subs(psiddot);
%psiddot = simplify(psiddot);

%}



%


%zdot = subs(zdot)';
%statedot = simplify(statedot);






%matlabFunction(zdot,"File","bi_steer_3D_Dynamics_full_1.m",Optimize=true);

dynamics_lin = [phidot, Vdot, phiddot, theta_Fdot, theta_Rdot]';
state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
U            = [    Tf, Tr, theta_Fdot, theta_Rdot];


JF_X = jacobian(F,state_lin);
JF_U = jacobian(F, U);


matlabFunction(JF_X,'File','JF_X.m','Optimize',true,'Comments','jacobian of F vector with states X');
matlabFunction(JF_U,'File','JF_U.m','Optimize',true, 'Comments','jacobian of F vecor with control input U');
matlabFunction(M,'File','Mass_matrix_M.m','Optimize',true);
matlabFunction(A,b,'File','A_b.m','Optimize',true);



%}



%}
